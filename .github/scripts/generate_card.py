#!/usr/bin/env python3
"""Render the neofetch-style profile card as light and dark SVGs.

Stats come from the GitHub GraphQL API at run time, so the committed SVGs
stay current without anything in the README needing to change. Two files are
written because GitHub picks between them with prefers-color-scheme.
"""

from __future__ import annotations

import json
import os
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

USER = "jainal09"
OUT_DIR = Path("assets")

QUERY = """
{
  user(login: "%s") {
    createdAt
    followers { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
      totalCount
      nodes { stargazerCount }
    }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      totalPullRequestContributions
    }
  }
}
""" % USER

# Left-hand emblem: a mesh, drawn with real primitives rather than box-drawing
# characters -- glyph cells are taller than they are wide, so text diagonals
# never land on the nodes. Coordinates are relative to the art origin.
NODES = [(60, 0), (140, 0), (20, 70), (100, 70), (180, 70), (60, 140), (140, 140)]
EDGES = [
    (0, 1), (0, 2), (0, 3), (1, 3), (1, 4), (2, 3),
    (3, 4), (2, 5), (3, 5), (3, 6), (4, 6), (5, 6),
]

THEMES = {
    "dark": {
        "bg": "#0d1117", "border": "#30363d", "text": "#c9d1d9",
        "dim": "#8b949e", "accent": "#58a6ff", "art": "#3fb950", "title": "#58a6ff",
    },
    "light": {
        "bg": "#ffffff", "border": "#d0d7de", "text": "#1f2328",
        "dim": "#656d76", "accent": "#0969da", "art": "#1a7f37", "title": "#0969da",
    },
}

SWATCHES = ["#f85149", "#db6d28", "#d29922", "#3fb950", "#58a6ff", "#bc8cff"]


def token() -> str:
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        return tok
    return subprocess.run(
        ["gh", "auth", "token"], capture_output=True, text=True, check=True
    ).stdout.strip()


def fetch() -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY}).encode(),
        headers={
            "Authorization": f"bearer {token()}",
            "Content-Type": "application/json",
            "User-Agent": f"{USER}-profile-card",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if "errors" in payload:
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    return payload["data"]["user"]


def humanise_uptime(created: str) -> str:
    start = datetime.fromisoformat(created.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    years = now.year - start.year
    months = now.month - start.month
    if now.day < start.day:
        months -= 1
    if months < 0:
        years -= 1
        months += 12
    return f"{years} years, {months} months"


def build_rows(user: dict) -> list[tuple[str, str]]:
    contrib = user["contributionsCollection"]
    commits = contrib["totalCommitContributions"] + contrib["restrictedContributionsCount"]
    stars = sum(n["stargazerCount"] for n in user["repositories"]["nodes"])
    # Quantitative only. The upstream work and envdrift have their own sections
    # in the README -- repeating them here made the page say everything twice.
    return [
        ("uptime", humanise_uptime(user["createdAt"])),
        ("repos", f"{user['repositories']['totalCount']} public"),
        ("stars", f"{stars}"),
        ("followers", f"{user['followers']['totalCount']}"),
        ("commits", f"{commits:,} this year"),
        ("pull requests", f"{contrib['totalPullRequestContributions']:,} this year"),
        # Deliberately not derived from repository language bytes. Measured that
        # way the top four are C++, Python, Swift, JavaScript -- C++ and Swift
        # are vendored/coursework weight, and Go disappears entirely because the
        # Go I write lands in nats-server and natscli, repos I do not own. Bytes
        # measure what is checked in, not what I work in.
        ("languages", "Python · Go · TypeScript · Java"),
        ("focus", "distributed systems · platform"),
    ]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(rows: list[tuple[str, str]], theme: dict) -> str:
    mono = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
    art_x, art_y, col_x, val_x = 40, 90, 280, 418
    top = 58
    line = 26

    # Size the canvas to the longest value rather than hard-coding a width.
    # Whichever monospace face the viewer actually resolves will have its own
    # advance width, so assume a generous 9.2px/char at 14px and pad -- a card
    # slightly too wide is invisible, a clipped one is obviously broken.
    longest = max(len(v) for _, v in rows)
    w = max(900, val_x + int(longest * 11) + 40)
    h = top + 42 + len(rows) * line + 46

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" font-family="{mono}" font-size="14">',
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" '
        f'fill="{theme["bg"]}" stroke="{theme["border"]}"/>',
    ]

    # window chrome, so it reads as a terminal at a glance
    for i, c in enumerate(("#f85149", "#d29922", "#3fb950")):
        out.append(f'<circle cx="{28 + i*20}" cy="26" r="6" fill="{c}"/>')
    out.append(
        f'<text x="{w//2}" y="31" text-anchor="middle" fill="{theme["dim"]}" '
        f'font-size="12">{USER} — profile</text>'
    )

    for a, b in EDGES:
        x1, y1 = NODES[a]
        x2, y2 = NODES[b]
        out.append(
            f'<line x1="{art_x+x1}" y1="{art_y+y1}" x2="{art_x+x2}" y2="{art_y+y2}" '
            f'stroke="{theme["art"]}" stroke-width="1.5" opacity="0.55"/>'
        )
    for x, y in NODES:
        out.append(
            f'<circle cx="{art_x+x}" cy="{art_y+y}" r="6" fill="{theme["bg"]}" '
            f'stroke="{theme["art"]}" stroke-width="2.5"/>'
        )

    out.append(
        f'<text x="{col_x}" y="{top}" fill="{theme["title"]}" font-weight="bold">'
        f'{USER}<tspan fill="{theme["dim"]}" font-weight="normal">@github</tspan></text>'
    )
    # A rule drawn as a <line>, not a run of U+2500. Repeated box-drawing
    # characters are the one part of this layout whose width depends on the
    # viewer having the same monospace font, so it is the one part that breaks
    # on someone else's machine. Everything else is positioned by x coordinate.
    out.append(
        f'<line x1="{col_x}" y1="{top + 12}" x2="{w - 40}" y2="{top + 12}" '
        f'stroke="{theme["border"]}" stroke-width="1"/>'
    )

    for i, (label, value) in enumerate(rows):
        y = top + 42 + i * line
        out.append(f'<text x="{col_x}" y="{y}" fill="{theme["accent"]}">{esc(label)}</text>')
        out.append(f'<text x="{val_x}" y="{y}" fill="{theme["text"]}">{esc(value)}</text>')

    for i, c in enumerate(SWATCHES):
        out.append(f'<rect x="{col_x + i*26}" y="{h-40}" width="20" height="12" rx="2" fill="{c}"/>')

    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    rows = build_rows(fetch())
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, theme in THEMES.items():
        path = OUT_DIR / f"card-{name}.svg"
        path.write_text(render(rows, theme), encoding="utf-8")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
