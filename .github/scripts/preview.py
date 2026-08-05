#!/usr/bin/env python3
"""Render README.md locally, the way GitHub will render it.

    python3 .github/scripts/preview.py

Markdown goes through GitHub's own /markdown API rather than a local library,
so the output is what the profile will actually show -- including which HTML
survives their sanitiser. Asset URLs are rewritten from raw.githubusercontent
to the working copy, so you preview the SVGs you just generated instead of
whatever is currently pushed.
"""

from __future__ import annotations

import json
import re
import subprocess
import webbrowser
from pathlib import Path

from generate_art import theme_variants

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".github" / "scripts" / "preview.html"
VARIANTS = ROOT / ".github" / "scripts" / ".preview-assets"
RAW = re.compile(
    r"https://raw\.githubusercontent\.com/jainal09/jainal09/[^/]+/(assets/[^\"'\s)]+)"
)

CSS = """
:root{--bg:#ffffff;--fg:#1f2328;--dim:#59636e;--line:#d1d9e0;--link:#0969da;--code:#818b981f}
body.dark{--bg:#0d1117;--fg:#e6edf3;--dim:#8b949e;--line:#3d444d;--link:#4493f8;--code:#6e768166}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
  font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
.bar{position:sticky;top:0;display:flex;gap:10px;align-items:center;padding:12px 20px;
  background:var(--bg);border-bottom:1px solid var(--line);font-size:13px;color:var(--dim);z-index:9}
.bar b{color:var(--fg);margin-right:auto;font-size:13px}
button{font:inherit;padding:5px 12px;border-radius:6px;cursor:pointer;
  background:transparent;color:var(--fg);border:1px solid var(--line)}
.page{max-width:1012px;margin:0 auto;padding:32px 16px 80px}
.md h1,.md h2{border-bottom:1px solid var(--line);padding-bottom:.3em;margin:24px 0 16px}
.md h1{font-size:2em}.md h2{font-size:1.5em}
.md a{color:var(--link);text-decoration:none}.md a:hover{text-decoration:underline}
.md img{max-width:100%}
.md table{border-collapse:collapse;margin:16px 0}
.md td,.md th{border:1px solid var(--line);padding:6px 13px}
.md tr:nth-child(2n){background:var(--code)}
.md code{background:var(--code);padding:.2em .4em;border-radius:6px;font-size:85%;
  font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.md blockquote{margin:0;padding:0 1em;color:var(--dim);border-left:.25em solid var(--line)}
.md hr{height:1px;background:var(--line);border:0;margin:24px 0}
.note{max-width:1012px;margin:0 auto;padding:0 16px 40px;color:var(--dim);font-size:13px}
"""

JS = """
function paint(dark){
  document.body.classList.toggle('dark', dark);
  for(const i of document.querySelectorAll('img[data-dark]'))
    i.src = (dark ? i.dataset.dark : i.dataset.light) + '?v=' + Date.now();
  for(const s of document.querySelectorAll('source[data-dark]'))
    s.srcset = (dark ? s.dataset.dark : s.dataset.light) + '?v=' + Date.now();
}
let dark = matchMedia('(prefers-color-scheme: dark)').matches;
document.getElementById('t').onclick=()=>{dark=!dark;paint(dark)};
document.getElementById('r').onclick=()=>location.reload();
paint(dark);
"""


def variants() -> None:
    """Bake each asset into an explicitly light and an explicitly dark copy.

    The SVGs decide their own colours from prefers-color-scheme, which reads
    the OS -- so a page-level toggle cannot move them, and the preview would
    happily show a dark graph on a white page and call it a preview. Resolving
    the media query ahead of time is the only way to see both without
    restarting into a different system appearance.
    """
    VARIANTS.mkdir(exist_ok=True)
    for src in sorted((ROOT / "assets").glob("*.svg")):
        if src.stem.endswith((".light", ".dark")):
            continue
        body = src.read_text(encoding="utf-8")
        light, dark = theme_variants(body)
        (VARIANTS / f"{src.stem}.light.svg").write_text(light, encoding="utf-8")
        (VARIANTS / f"{src.stem}.dark.svg").write_text(dark, encoding="utf-8")


def preview_asset(match: re.Match) -> str:
    """Map production theme variants back to one locally switchable source."""
    stem = Path(match.group(1)).stem
    if stem.endswith((".light", ".dark")):
        stem = stem.rsplit(".", 1)[0]
    return (f'.preview-assets/{stem}.light.svg" '
            f'data-dark=".preview-assets/{stem}.dark.svg" '
            f'data-light=".preview-assets/{stem}.light.svg')


def render(md: str) -> str:
    out = subprocess.run(
        ["gh", "api", "markdown", "-f", "mode=gfm", "-f", f"text={md}"],
        capture_output=True, text=True, check=True,
    )
    return out.stdout


def main() -> None:
    md = (ROOT / "README.md").read_text(encoding="utf-8")
    html = render(md)
    # Point at the working copy so local regeneration is what you see.
    variants()
    # Point every asset at its baked light copy, and remember the dark one so
    # the toggle can swap both the page and the artwork together.
    html = RAW.sub(preview_asset, html)

    OUT.write_text(
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<title>README preview</title><style>" + CSS + "</style></head><body>"
        "<div class='bar'><b>README preview — local assets</b>"
        "<button id='t'>page theme</button><button id='r'>reload</button></div>"
        "<div class='page'><div class='md'>" + html + "</div></div>"
        "<p class='note'>The theme button switches the page <em>and</em> the "
        "artwork together. Each SVG is baked into an explicitly light and dark "
        "copy, because prefers-color-scheme reads your OS and no page-level "
        "toggle can reach it — which is exactly how a preview ends up showing a "
        "dark graph on a white page.</p>"
        "<script>" + JS + "</script></body></html>",
        encoding="utf-8",
    )
    print(f"wrote {OUT}")
    webbrowser.open(OUT.as_uri())


if __name__ == "__main__":
    main()
