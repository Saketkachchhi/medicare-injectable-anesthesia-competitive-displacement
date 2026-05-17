#!/usr/bin/env python3
"""
html_to_ipynb.py
================

Reverse-engineer a JupyterLab `nbconvert`-exported HTML file back into a clean,
fully functional Jupyter Notebook (`.ipynb`).

Designed for the BIA-810 Healthcare Analytics End-Term submission
(`Healthcare_Analytics_End_Term_FINAL.html`), but it works against any standard
JupyterLab HTML export that uses the `jp-Cell` / `jp-CodeCell` / `jp-MarkdownCell`
CSS contract.

What it does
------------
1. Parses the HTML with `BeautifulSoup`.
2. Walks every `.jp-Cell` container in document order.
3. For **code cells** it pulls the verbatim source out of the `.jp-CodeMirrorEditor`
   block, strips the `In [n]:` prompt artifact, and writes it back as a code cell.
4. For **markdown cells** it recursively converts the rendered HTML
   (`.jp-RenderedMarkdown`) back into clean Markdown source — preserving
   headings, ordered/unordered lists, GitHub-flavored pipe tables,
   blockquotes, bold/italic, inline code, fenced code, links, and images.
5. Emits a valid `nbformat 4.5` JSON document. No `nbformat` package required;
   only the standard library + `beautifulsoup4`.

Usage
-----
    python html_to_ipynb.py \\
        --input  Healthcare_Analytics_End_Term_FINAL.html \\
        --output Healthcare_Analytics_End_Term_FINAL.ipynb

Or with positional arguments:

    python html_to_ipynb.py Healthcare_Analytics_End_Term_FINAL.html out.ipynb

Dependencies
------------
    pip install beautifulsoup4

Author: J-FIVE Healthcare Commercial Analytics Team
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup, NavigableString, Tag


# ----------------------------------------------------------------------------- #
# Code-cell extraction
# ----------------------------------------------------------------------------- #
def extract_code_source(cell: Tag) -> str:
    """Pull the raw Python source from a `.jp-CodeCell` container."""
    editor = cell.select_one(".jp-CodeMirrorEditor") or cell.select_one(
        ".jp-InputArea-editor"
    )
    if editor is None:
        # Fallback: many older nbconvert templates use <div class="input"> + <pre>
        pre = cell.find("pre")
        return pre.get_text() if pre else ""

    # Preferred path: editor wraps a <pre> with line-broken source
    pre = editor.find("pre")
    text = pre.get_text() if pre else editor.get_text()

    # nbconvert sometimes prefixes a blank line; trim that and trailing whitespace.
    return text.lstrip("\n").rstrip()


# ----------------------------------------------------------------------------- #
# Markdown-cell extraction (recursive HTML → Markdown)
# ----------------------------------------------------------------------------- #
def node_to_md(node) -> str:
    """Recursively convert a BeautifulSoup node back into Markdown source."""
    if isinstance(node, NavigableString):
        return str(node)

    name = node.name
    children = list(node.children)

    # ---- Headings ---------------------------------------------------------- #
    if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
        # Strip JupyterLab anchor links and the pilcrow (¶) that nbconvert adds.
        for anchor in node.find_all(
            "a", class_=lambda c: c and "anchor-link" in c
        ):
            anchor.decompose()
        level = int(name[1])
        text = "".join(node_to_md(c) for c in node.children).strip()
        text = text.replace("¶", "").strip()
        return f"\n{'#' * level} {text}\n\n"

    # ---- Paragraphs -------------------------------------------------------- #
    if name == "p":
        text = "".join(node_to_md(c) for c in children).strip()
        return f"{text}\n\n"

    # ---- Inline formatting ------------------------------------------------- #
    if name in ("strong", "b"):
        return "**" + "".join(node_to_md(c) for c in children) + "**"

    if name in ("em", "i"):
        return "*" + "".join(node_to_md(c) for c in children) + "*"

    if name == "code":
        return "`" + node.get_text() + "`"

    # ---- Fenced code blocks ----------------------------------------------- #
    if name == "pre":
        return "\n```\n" + node.get_text().rstrip() + "\n```\n\n"

    # ---- Lists ------------------------------------------------------------- #
    if name == "ul":
        out = ["\n"]
        for li in node.find_all("li", recursive=False):
            line = "".join(node_to_md(c) for c in li.children).strip()
            out.append(f"- {line}\n")
        out.append("\n")
        return "".join(out)

    if name == "ol":
        out = ["\n"]
        for idx, li in enumerate(node.find_all("li", recursive=False), 1):
            line = "".join(node_to_md(c) for c in li.children).strip()
            out.append(f"{idx}. {line}\n")
        out.append("\n")
        return "".join(out)

    # ---- Line breaks ------------------------------------------------------- #
    if name == "br":
        return "  \n"

    # ---- Links & images ---------------------------------------------------- #
    if name == "a":
        if "anchor-link" in (node.get("class") or []):
            return ""
        href = node.get("href", "")
        text = "".join(node_to_md(c) for c in children).strip()
        return f"[{text}]({href})" if href else text

    if name == "img":
        alt = node.get("alt", "")
        src = node.get("src", "")
        return f"![{alt}]({src})"

    # ---- Tables (rendered as GitHub-flavored pipe tables) ----------------- #
    if name == "table":
        return table_to_md(node) + "\n"

    # Skip table sub-elements at the top level; they are handled inside
    # `table_to_md` so they never get double-rendered.
    if name in ("thead", "tbody", "tr", "td", "th"):
        return ""

    # ---- Blockquotes & horizontal rules ----------------------------------- #
    if name == "blockquote":
        text = "".join(node_to_md(c) for c in children).strip()
        return "\n> " + text.replace("\n", "\n> ") + "\n\n"

    if name == "hr":
        return "\n---\n\n"

    # ---- Default: descend into children ----------------------------------- #
    return "".join(node_to_md(c) for c in children)


def table_to_md(table: Tag) -> str:
    """Render a <table> as a GitHub-flavored Markdown pipe table."""
    rows: List[List[str]] = []
    for tr in table.find_all("tr"):
        cells: List[str] = []
        for cell in tr.find_all(["td", "th"]):
            cell_text = "".join(node_to_md(c) for c in cell.children)
            cell_text = re.sub(r"\s+", " ", cell_text).strip()
            cell_text = cell_text.replace("|", r"\|")
            cells.append(cell_text)
        if cells:
            rows.append(cells)

    if not rows:
        return ""

    width = max(len(r) for r in rows)
    header = rows[0] + [""] * (width - len(rows[0]))
    body = [r + [""] * (width - len(r)) for r in rows[1:]]

    out = ["\n| " + " | ".join(header) + " |"]
    out.append("| " + " | ".join(["---"] * width) + " |")
    for r in body:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out) + "\n"


# ----------------------------------------------------------------------------- #
# Notebook assembly
# ----------------------------------------------------------------------------- #
def source_as_lines(text: str) -> List[str]:
    """ipynb v4 stores source as a list of lines (each ending in '\\n')."""
    if not text:
        return []
    return text.splitlines(keepends=True)


def html_to_notebook(html_path: Path) -> dict:
    """Parse the HTML file and return a notebook dict ready to JSON-dump."""
    html = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    cell_nodes = soup.select(".jp-Cell")

    if not cell_nodes:
        raise SystemExit(
            "ERROR: No `.jp-Cell` containers found. This script is built for "
            "JupyterLab nbconvert HTML exports. Verify the input file."
        )

    cells = []
    for node in cell_nodes:
        classes = node.get("class", [])

        if "jp-CodeCell" in classes:
            src = extract_code_source(node)
            cells.append(
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": source_as_lines(src),
                }
            )

        elif "jp-MarkdownCell" in classes:
            md_root = node.select_one(".jp-RenderedMarkdown") or node.select_one(
                ".jp-RenderedHTMLCommon"
            )
            if md_root is None:
                continue
            md_src = "".join(node_to_md(c) for c in md_root.children).strip() + "\n"
            # Collapse any run of 3+ blank lines down to a single blank line.
            md_src = re.sub(r"\n{3,}", "\n\n", md_src)
            cells.append(
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": source_as_lines(md_src),
                }
            )

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.x",
                "mimetype": "text/x-python",
                "file_extension": ".py",
                "pygments_lexer": "ipython3",
                "codemirror_mode": {"name": "ipython", "version": 3},
                "nbconvert_exporter": "python",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


# ----------------------------------------------------------------------------- #
# CLI entry point
# ----------------------------------------------------------------------------- #
def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Convert a JupyterLab nbconvert HTML export back into a .ipynb."
    )
    p.add_argument(
        "input",
        nargs="?",
        help="Path to the input HTML file (e.g. Healthcare_Analytics_End_Term_FINAL.html).",
    )
    p.add_argument(
        "output",
        nargs="?",
        help="Path to write the reconstructed .ipynb to.",
    )
    p.add_argument("--input", "-i", dest="input_flag", help=argparse.SUPPRESS)
    p.add_argument("--output", "-o", dest="output_flag", help=argparse.SUPPRESS)
    args = p.parse_args(argv)

    in_path = args.input_flag or args.input
    out_path = args.output_flag or args.output

    if not in_path:
        p.error("input HTML path is required")
    if not out_path:
        # Default: same stem, .ipynb extension, written next to the input.
        out_path = str(Path(in_path).with_suffix(".ipynb"))

    return Path(in_path), Path(out_path)


def main(argv=None) -> int:
    in_path, out_path = parse_args(argv)
    if not in_path.exists():
        print(f"ERROR: input file not found: {in_path}", file=sys.stderr)
        return 1

    notebook = html_to_notebook(in_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    code_count = sum(1 for c in notebook["cells"] if c["cell_type"] == "code")
    md_count = sum(1 for c in notebook["cells"] if c["cell_type"] == "markdown")
    print(
        f"[OK] Wrote {out_path}  "
        f"(cells={len(notebook['cells'])}, code={code_count}, markdown={md_count})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
