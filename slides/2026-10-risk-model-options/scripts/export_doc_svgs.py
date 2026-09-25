#!/usr/bin/env python3
"""Export the deck's SVG visuals as standalone files for the MkDocs page.

The Vue components in ../components are the single source of each visual. This
script renders the running slidev dev server in headless Chrome, extracts each
<svg role="img"> by its aria-label, inlines the component's scoped CSS and a font
stack, and writes docs/model/img/risk-model/<name>.svg.

Usage (from this deck's folder, with the dev server running):
    pnpm dev --port 3031          # in another terminal
    python3 scripts/export_doc_svgs.py [--url http://localhost:3031] [--chrome google-chrome]
"""
import argparse
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# aria-label prefix -> output file name
TARGETS = {
    "Risk is where hazard": "risk-intro.svg",
    "A hazard occurrence sits": "hazard-meanings.svg",
    "Arguments of the risk function": "risk-function.svg",
    "People and buildings inside": "key-test.svg",
    "Population funnel": "pin-funnel.svg",
    "Context layers stacked": "context-layers.svg",
    "Roadmap of five": "level-roadmap.svg",
    "NOUL-26 population": "noul26-exposure.svg",
    "Population exposed by shaking": "tibet-mmi-exposure.svg",
}
FONT = 'svg { font-family: Roboto, "Helvetica Neue", Arial, sans-serif; }'
OUT = Path(__file__).resolve().parents[3] / "docs" / "model" / "img" / "risk-model"


def dump(url: str, chrome: str) -> str:
    cmd = [chrome, "--headless=new", "--disable-gpu", "--virtual-time-budget=9000", "--dump-dom", url]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=120).stdout


def standalone(svg: str, styles: list[str]) -> str:
    vid = re.search(r"data-v-([0-9a-f]{8})", svg)
    css = [FONT]
    if vid:
        css += [s for s in styles if f"data-v-{vid.group(1)}" in s]
    vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg)
    size = f' width="{vb.group(1)}" height="{vb.group(2)}"' if vb else ""
    svg = svg.replace(' class="w-full"', "", 1)
    svg = re.sub(r"^<svg", f'<svg xmlns="http://www.w3.org/2000/svg"{size}', svg, count=1)
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S).replace("&nbsp;", "&#160;")
    head, rest = svg.split(">", 1)
    return f'{head}><style>{" ".join(css)}</style>{rest}\n'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://localhost:3031")
    ap.add_argument("--chrome", default="google-chrome")
    ap.add_argument("--max-slides", type=int, default=40)
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    todo = dict(TARGETS)
    for n in range(1, args.max_slides + 1):
        if not todo:
            break
        html = dump(f"{args.url}/{n}?embedded=true", args.chrome)
        styles = re.findall(r"<style[^>]*>(.*?)</style>", html, flags=re.S)
        for svg in re.findall(r'<svg[^>]*role="img"[^>]*>.*?</svg>', html, flags=re.S):
            label = re.search(r'aria-label="([^"]*)"', svg)
            key = next((k for k in todo if label and label.group(1).startswith(k)), None)
            if not key:
                continue
            out = standalone(svg, styles)
            ET.fromstring(out)  # must be well-formed XML
            (OUT / todo.pop(key)).write_text(out, encoding="utf-8")
            print(f"slide {n}: {key!r} -> {TARGETS[key]}")
    if todo:
        print(f"missing: {sorted(todo.values())}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
