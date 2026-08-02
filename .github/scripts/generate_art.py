#!/usr/bin/env python3
"""Render the profile's two hand-drawn SVGs.

Both share one palette so the page reads as designed rather than assembled.
Every colour is a mid-tone that holds on GitHub's light and dark themes, and
neither file paints a background -- so there is no prefers-color-scheme swap
to fail, and no theme it fails on.

  cluster.svg  message flow through a NATS cluster (Open Source)
  stack.svg    a request descending the layers I work in (About)
"""

from __future__ import annotations

from pathlib import Path

OUT_DIR = Path("assets")

GREEN = "#3fb950"
BLUE = "#4c8eda"
DIM = "#7d8590"
EDGE = "#8b949e"

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"


def svg_open(w: int, h: int) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" font-family="{MONO}" fill="none">'
    )


def text(x, y, body, fill=DIM, size=13, weight="normal") -> str:
    # Left-anchored at an explicit x throughout. text-anchor="end" puts the
    # right edge of the string at the mercy of whichever monospace face the
    # viewer resolves, and an overrun here is clipped by the viewBox.
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" '
        f'font-weight="{weight}">{body}</text>'
    )


# ---------------------------------------------------------------- cluster ---

CW, CH = 980, 300
PUBS = [(70, 80), (70, 220)]
CORE = [(330, 70), (330, 230), (470, 150)]
SUBS = [(850, 80), (850, 220)]

FLOWS = [
    (PUBS[0], CORE[0], 0.0), (PUBS[1], CORE[1], 1.1),
    (CORE[0], CORE[2], 0.4), (CORE[1], CORE[2], 1.5), (CORE[0], CORE[1], 2.1),
    (CORE[2], SUBS[0], 0.9), (CORE[2], SUBS[1], 1.9),
]
LINKS = [
    (PUBS[0], CORE[0]), (PUBS[1], CORE[1]),
    (CORE[0], CORE[1]), (CORE[0], CORE[2]), (CORE[1], CORE[2]),
    (CORE[2], SUBS[0]), (CORE[2], SUBS[1]),
]


def cluster() -> str:
    s = [svg_open(CW, CH)]
    for (x1, y1), (x2, y2) in LINKS:
        s.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{EDGE}" '
            f'stroke-width="1" opacity="0.35"/>'
        )
    for i, ((x1, y1), (x2, y2), delay) in enumerate(FLOWS):
        s.append(f'<path id="f{i}" d="M{x1},{y1} L{x2},{y2}" stroke="none"/>')
        s.append(
            f'<circle r="3.5" fill="{GREEN}">'
            f'<animateMotion dur="2.4s" begin="{delay}s" repeatCount="indefinite" '
            f'keyPoints="0;1" keyTimes="0;1" calcMode="linear">'
            # both spellings: SVG 1.1 renderers ignore bare href and the
            # packets would simply never move.
            f'<mpath href="#f{i}" xlink:href="#f{i}"/></animateMotion>'
            f'<animate attributeName="opacity" values="0;1;1;0" dur="2.4s" '
            f'begin="{delay}s" repeatCount="indefinite"/></circle>'
        )
    for x, y in PUBS + SUBS:
        s.append(f'<circle cx="{x}" cy="{y}" r="7" stroke="{BLUE}" stroke-width="2"/>')
    for i, (x, y) in enumerate(CORE):
        s.append(
            f'<circle cx="{x}" cy="{y}" r="11" stroke="{GREEN}" stroke-width="2">'
            f'<animate attributeName="r" values="11;13;11" dur="3s" '
            f'begin="{i * 0.7}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="1;0.55;1" dur="3s" '
            f'begin="{i * 0.7}s" repeatCount="indefinite"/></circle>'
        )
    s += [
        text(52, 30, "publishers", DIM, 11),
        text(360, 30, "cluster", GREEN, 11),
        text(780, 30, "subscribers", DIM, 11),
        text(52, 272, "5.0M msg/s", GREEN, 15, "bold"),
        text(160, 272, "measured by knack on constrained hardware", DIM, 12),
        text(520, 272, "shipped: nats-server 2.14.4 · nui 0.9.3", BLUE, 12),
    ]
    return "\n".join(s) + "\n</svg>"


# ------------------------------------------------------------------ stack ---

SW, SH = 980, 304
LAYERS = [
    # A clients layer so the stack spans client to state. Without it the
    # drawing reads as an exhaustive list of what I touch, which it is not --
    # Swift and C++ are both larger in bytes than most of what is named here.
    ("clients", "Swift · TypeScript · React"),
    ("edge", "FastAPI · Spring Boot"),
    ("broker", "Kafka · NATS JetStream"),
    ("workers", "Celery · consumers"),
    ("state", "Postgres · Redis"),
]
CYCLE = 5.2
RAIL_X = 44
BAND_X, BAND_W, BAND_H, GAP = 76, 860, 40, 12
TOP = 40


def stack() -> str:
    s = [svg_open(SW, SH)]
    span = len(LAYERS) * (BAND_H + GAP) - GAP

    s.append(
        f'<line x1="{RAIL_X}" y1="{TOP}" x2="{RAIL_X}" y2="{TOP + span}" '
        f'stroke="{EDGE}" stroke-width="1" opacity="0.3"/>'
    )

    for i, (layer, tech) in enumerate(LAYERS):
        y = TOP + i * (BAND_H + GAP)
        # Each band lights as the descending request reaches it. Offsetting
        # begin by i keeps one pulse travelling rather than four blinking.
        begin = round(i * (CYCLE / len(LAYERS)), 2)
        s.append(
            f'<rect x="{BAND_X}" y="{y}" width="{BAND_W}" height="{BAND_H}" rx="6" '
            f'stroke="{EDGE}" stroke-width="1" opacity="0.28">'
            f'<animate attributeName="opacity" values="0.28;0.85;0.28" '
            f'dur="{CYCLE}s" begin="{begin}s" repeatCount="indefinite"/></rect>'
        )
        s.append(
            f'<circle cx="{RAIL_X}" cy="{y + BAND_H // 2}" r="4" fill="{GREEN}" '
            f'opacity="0.25"><animate attributeName="opacity" '
            f'values="0.25;1;0.25" dur="{CYCLE}s" begin="{begin}s" '
            f'repeatCount="indefinite"/></circle>'
        )
        s.append(text(BAND_X + 24, y + 26, layer, BLUE, 13, "bold"))
        # Pushed right so the band reads as a spanned row rather than a label
        # with 380px of dead space after it.
        s.append(text(BAND_X + 520, y + 26, tech, DIM, 13))

    # The request itself. The staggered band pulses imply the descent; this
    # makes it literal, which is the whole point of the caption.
    s.append(
        f'<circle cx="{RAIL_X}" r="5" fill="{GREEN}">'
        f'<animate attributeName="cy" values="{TOP};{TOP + span}" dur="{CYCLE}s" '
        f'repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0;1;1;0" dur="{CYCLE}s" '
        f'repeatCount="indefinite"/></circle>'
    )

    s.append(text(BAND_X, 24, "a request, on the way down", DIM, 11))
    return "\n".join(s) + "\n</svg>"


# --------------------------------------------------------------- trophies ---

TW, TH = 980, 214
TCOLS = 4
TM, TCOL = 40, 225
TROW = [64, 152]


def trophies(stats: dict) -> str:
    """The same information the trophy row carried, in this design system.

    No rank letters and no progress bars: a bar needs a scale, and inventing
    one to make a number look like an achievement is how the original reads
    as a video game. Label, figure, rule.
    """
    tiles = [
        ("commits", f"{stats['commits_yr']:,}", "this year"),
        ("pull requests", f"{stats['prs_total']:,}", "opened"),
        ("issues", f"{stats['issues_total']:,}", "opened"),
        ("repositories", f"{stats['repos']}", "public, non-fork"),
        ("stars", f"{stats['stars']}", "received"),
        ("followers", f"{stats['followers']}", ""),
        ("organisations", f"{stats['orgs']}", ""),
        ("on github", f"{stats['years']}", "years"),
    ]
    s = [svg_open(TW, TH)]
    for i, (label, value, note) in enumerate(tiles):
        x = TM + (i % TCOLS) * TCOL
        y = TROW[i // TCOLS]
        s.append(text(x, y - 22, label, DIM, 11))
        s.append(text(x, y + 8, value, GREEN, 25, "bold"))
        if note:
            s.append(text(x + len(value) * 16 + 10, y + 8, note, DIM, 11))
        # Rule draws in once and freezes. Decorative, and deliberately the
        # same width everywhere so it cannot be misread as a proportion.
        # Authored at full width and animated up from zero, so a renderer that
        # ignores SMIL shows the finished rule rather than nothing at all.
        s.append(
            f'<line x1="{x}" y1="{y + 24}" x2="{x + 168}" y2="{y + 24}" '
            f'stroke="{BLUE}" stroke-width="2" opacity="0.6">'
            f'<animate attributeName="x2" from="{x}" to="{x + 168}" dur="0.7s" '
            f'begin="{round(i * 0.08, 2)}s" fill="freeze"/></line>'
        )
    return "\n".join(s) + "\n</svg>"


def fetch_stats() -> dict:
    import json, os, subprocess, urllib.request
    from datetime import datetime, timezone

    q = """{ user(login:"jainal09"){ createdAt followers{totalCount}
      organizations{totalCount}
      repositories(first:100, ownerAffiliations:OWNER, isFork:false){
        totalCount nodes{ stargazerCount } }
      contributionsCollection{ totalCommitContributions restrictedContributionsCount }
      pullRequests{totalCount} issues{totalCount} } }"""
    tok = os.environ.get("GITHUB_TOKEN") or subprocess.run(
        ["gh", "auth", "token"], capture_output=True, text=True, check=True
    ).stdout.strip()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": q}).encode(),
        headers={"Authorization": f"bearer {tok}", "Content-Type": "application/json",
                 "User-Agent": "jainal09-profile-art"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    u = payload["data"]["user"]
    c = u["contributionsCollection"]
    start = datetime.fromisoformat(u["createdAt"].replace("Z", "+00:00"))
    return {
        "commits_yr": c["totalCommitContributions"] + c["restrictedContributionsCount"],
        "prs_total": u["pullRequests"]["totalCount"],
        "issues_total": u["issues"]["totalCount"],
        "repos": u["repositories"]["totalCount"],
        "stars": sum(n["stargazerCount"] for n in u["repositories"]["nodes"]),
        "followers": u["followers"]["totalCount"],
        "orgs": u["organizations"]["totalCount"],
        "years": (datetime.now(timezone.utc) - start).days // 365,
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, body in (("cluster", cluster()), ("stack", stack()),
                       ("trophies", trophies(fetch_stats()))):
        path = OUT_DIR / f"{name}.svg"
        path.write_text(body, encoding="utf-8")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
