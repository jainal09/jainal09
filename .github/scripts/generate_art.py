#!/usr/bin/env python3
"""Render the profile's desktop and mobile SVGs.

Desktop and mobile variants consume the same live data and share one palette,
so responsive layout changes do not fork the design system or leave scheduled
renders updating only half of the profile. Theme-aware files carry their own
``prefers-color-scheme`` rules for GitHub's light and dark canvases.
"""

from __future__ import annotations

from pathlib import Path
from textwrap import wrap

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


def esc(s: str) -> str:
    """XML-escape. Every string here is escaped at the single point it becomes
    markup, rather than at each call site -- track and artist names are the one
    input I do not control, and a bare & in "Jonathan & Friends" does not
    degrade, it makes the whole file unparseable.
    """
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def text(x, y, body, fill=DIM, size=13, weight="normal", cls=None,
         anchor=None, clip=None) -> str:
    # Left-anchored by default. Centred diagram headings and compact mobile
    # status labels opt into an anchor where the available width is bounded.
    return (
        f'<text x="{x}" y="{y}"'
        + (f' class="{cls}"' if cls else f' fill="{fill}"')
        + (f' text-anchor="{anchor}"' if anchor else "")
        + (f' clip-path="url(#{clip})"' if clip else "")
        + f' font-size="{size}" font-weight="{weight}">{esc(body)}</text>'
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


def cluster_mobile() -> str:
    """The same topology, reflowed vertically so labels stay readable."""
    w, h = 390, 456
    pubs = [(110, 58), (280, 58)]
    core = [(130, 165), (260, 165), (195, 245)]
    subs = [(110, 335), (280, 335)]
    links = [
        (pubs[0], core[0]), (pubs[1], core[1]),
        (core[0], core[1]), (core[0], core[2]), (core[1], core[2]),
        (core[2], subs[0]), (core[2], subs[1]),
    ]
    flows = [
        (pubs[0], core[0], 0.0), (pubs[1], core[1], 1.1),
        (core[0], core[2], 0.45), (core[1], core[2], 1.55),
        (core[2], subs[0], 0.9), (core[2], subs[1], 1.9),
    ]
    style = """<style>
  .background{fill:#ffffff}.line{stroke:#8b949e}.muted{fill:#59636e}.blue{fill:#4c8eda}
  @media (prefers-color-scheme: dark){.background{fill:#0d1117}.muted{fill:#8b949e}}
</style>"""
    s = [svg_open(w, h), style]
    s += [
        text(195, 24, "publishers", None, 14, cls="muted", anchor="middle"),
        text(195, 125, "NATS cluster", GREEN, 14, anchor="middle"),
    ]
    for (x1, y1), (x2, y2) in links:
        s.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'class="line" stroke-width="1.5" opacity="0.45"/>'
        )
    for i, ((x1, y1), (x2, y2), delay) in enumerate(flows):
        s.append(f'<path id="mf{i}" d="M{x1},{y1} L{x2},{y2}" stroke="none"/>')
        s.append(
            f'<circle r="4" fill="{GREEN}" opacity="0">'
            f'<animateMotion dur="2.4s" begin="{delay}s" repeatCount="indefinite">'
            f'<mpath href="#mf{i}" xlink:href="#mf{i}"/></animateMotion>'
            f'<animate attributeName="opacity" values="0;1;1;0" dur="2.4s" '
            f'begin="{delay}s" repeatCount="indefinite"/></circle>'
        )
    # The label masks the two diagonal links; otherwise they cut through the
    # word on a narrow canvas. The mask follows the page theme.
    s.append('<rect x="137" y="288" width="116" height="25" rx="4" class="background"/>')
    s.append(text(195, 305, "subscribers", None, 14, cls="muted", anchor="middle"))
    for x, y in pubs + subs:
        s.append(f'<circle cx="{x}" cy="{y}" r="10" stroke="{BLUE}" stroke-width="2.5"/>')
    for i, (x, y) in enumerate(core):
        s.append(
            f'<circle cx="{x}" cy="{y}" r="14" stroke="{GREEN}" stroke-width="2.5">'
            f'<animate attributeName="r" values="14;17;14" dur="3s" '
            f'begin="{round(i * 0.7, 2)}s" repeatCount="indefinite"/></circle>'
        )
    s += [
        text(24, 388, "5.0M msg/s", GREEN, 18, "bold"),
        text(24, 412, "measured by knack on constrained hardware", None, 13, cls="muted"),
        text(24, 440, "shipped: nats-server 2.14.4 · nui 0.9.3", None, 13, cls="blue"),
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


def stack_mobile() -> str:
    """Stack labels and technologies within each row instead of shrinking it."""
    w, h = 390, 374
    rail_x, band_x, top = 20, 48, 30
    band_w, band_h, gap = 324, 58, 10
    style = """<style>
  .rail,.card{stroke:#8b949e}.label{fill:#4c8eda}.detail,.caption{fill:#59636e}
  @media (prefers-color-scheme: dark){.detail,.caption{fill:#8b949e}}
</style>"""
    s = [svg_open(w, h), style]
    s.append(text(band_x, 18, "a request, on the way down", None, 13, cls="caption"))
    s.append(f'<line x1="{rail_x}" y1="{top}" x2="{rail_x}" y2="360" '
             f'class="rail" stroke-width="1" opacity="0.35"/>')
    for i, (layer, tech) in enumerate(LAYERS):
        y = top + i * (band_h + gap)
        begin = round(i * (CYCLE / len(LAYERS)), 2)
        s.append(
            f'<rect x="{band_x}" y="{y}" width="{band_w}" height="{band_h}" rx="7" '
            f'class="card" stroke-width="1" opacity="0.35">'
            f'<animate attributeName="opacity" values="0.35;0.9;0.35" '
            f'dur="{CYCLE}s" begin="{begin}s" repeatCount="indefinite"/></rect>'
        )
        s.append(
            f'<circle cx="{rail_x}" cy="{y + band_h // 2}" r="5" fill="{GREEN}" '
            f'opacity="0.3"><animate attributeName="opacity" values="0.3;1;0.3" '
            f'dur="{CYCLE}s" begin="{begin}s" repeatCount="indefinite"/></circle>'
        )
        s.append(text(band_x + 18, y + 24, layer, None, 15, "bold", cls="label"))
        s.append(text(band_x + 18, y + 46, tech, None, 14, cls="detail"))
    s.append(
        f'<circle cx="{rail_x}" r="6" fill="{GREEN}">'
        f'<animate attributeName="cy" values="{top};360" dur="{CYCLE}s" '
        f'repeatCount="indefinite"/><animate attributeName="opacity" '
        f'values="0;1;1;0" dur="{CYCLE}s" repeatCount="indefinite"/></circle>'
    )
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


# ------------------------------------------------------------------ music ---

MW = 980
COLS, ROWS = 32, 7
CELL_W, CELL_H, CELL_GX, CELL_GY = 20, 10, 6, 4
LED_X = (MW - (COLS * CELL_W + (COLS - 1) * CELL_GX)) // 2
LED_Y = 26
STEPS = 16
# Painted with GitHub's own canvas colours and switched by an internal media
# query, so the panel reads as part of the page instead of a black slab on it.
# One file rather than a two-file <picture> swap: the 16 covers are inlined as
# base64, and a second variant would duplicate every byte of them.
SCREEN_STYLE = """<style>
  .bg{fill:#ffffff}.lit{fill:#1f2328}.unlit{fill:#d0d7de}
  .mut{fill:#656d76}.quirk{fill:#8c959f}
  @media (prefers-color-scheme: dark){
    .bg{fill:#0d1117}.lit{fill:#e6edf3}.unlit{fill:#21262d}
    .mut{fill:#8b949e}.quirk{fill:#6e7681}
  }
</style>"""

RANGES = [("all time", "long_term"), ("last 6 months", "medium_term"),
          ("last 4 weeks", "short_term")]
COL_W, COL_GAP, ART, ROW_H = 300, 20, 34, 46


def _levels(col: int) -> list[int]:
    """Deterministic level sequence per column.

    Deterministic on purpose: this file regenerates daily, and randomising the
    animation would produce a diff every run and churn history for nothing.
    """
    seq, x = [], (col * 2654435761) & 0xFFFFFFFF
    for _ in range(STEPS):
        x = (x * 1103515245 + 12345) & 0x7FFFFFFF
        seq.append(1 + (x >> 16) % ROWS)
    return seq


def _art(uri: str | None, x: int, y: int, size: int) -> str:
    """Album art must be inlined as a data: URI.

    An SVG loaded through <img> runs under a CSP of img-src data: -- a remote
    <image href="https://..."> renders as nothing at all. So the bytes travel
    inside the file or they do not arrive.
    """
    if not uri:
        return (f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="3" '
                f'class="unlit"/>')
    return (f'<image x="{x}" y="{y}" width="{size}" height="{size}" '
            f'href="{uri}" xlink:href="{uri}" preserveAspectRatio="xMidYMid slice"/>')


def music(data: dict | None) -> str:
    tops = (data or {}).get("tops") or {}
    rows = max([len(tops.get(k, [])) for _, k in RANGES] + [0])
    head = LED_Y + ROWS * (CELL_H + CELL_GY) + 18
    cols_y = head + 118
    height = cols_y + 24 + rows * ROW_H + 34 if rows else head + 116

    s = [svg_open(MW, height), SCREEN_STYLE]
    s.append(f'<rect x="0" y="0" width="{MW}" height="{height}" rx="10" class="bg"/>')

    # A black screen on both themes deliberately: a device on the page, not a
    # panel that failed to pick up the background.
    for c in range(COLS):
        seq = _levels(c)
        x = LED_X + c * (CELL_W + CELL_GX)
        dur = round(1.5 + (c % 5) * 0.17, 2)
        for r in range(ROWS):
            y = LED_Y + (ROWS - 1 - r) * (CELL_H + CELL_GY)
            vals = ";".join("1" if lvl > r else "0.14" for lvl in seq)
            s.append(
                f'<rect x="{x}" y="{y}" width="{CELL_W}" height="{CELL_H}" rx="1.5" '
                f'class="lit" opacity="0.14">'
                f'<animate attributeName="opacity" values="{vals}" dur="{dur}s" '
                f'calcMode="discrete" repeatCount="indefinite"/></rect>'
            )

    now = (data or {}).get("now")
    if now:
        title, artist, pct, label = now["title"], now["artist"], now["pct"], now["label"]
        quirk = "you may now appreciate my taste in music"
        art = now.get("art")
    else:
        title, artist, pct, label, art = "— not connected —", "", 0.0, "", None
        quirk = "looks like my OAuth token expired. it does that."

    s.append(text(LED_X, head + 4, now and "now playing" or "status", None, 11, cls="mut"))
    s.append(_art(art, LED_X, head + 14, 56))
    s.append(text(LED_X + 70, head + 36, title[:44], None, 15, "bold", cls="lit"))
    s.append(text(LED_X + 70, head + 58, artist[:52], None, 12, cls="mut"))

    blocks, bx, by = 46, LED_X + 70, head + 72
    filled = round(pct * blocks)
    for i in range(blocks):
        s.append(f'<rect x="{bx + i * 13}" y="{by}" width="9" height="9" '
                 f'class="{"lit" if i < filled else "unlit"}"/>')
    if label:
        s.append(text(bx + blocks * 13 + 12, by + 9, label, None, 11, cls="mut"))
    s.append(text(LED_X, head + 100, quirk, None, 11, cls="quirk"))

    if rows:
        cx0 = (MW - (3 * COL_W + 2 * COL_GAP)) // 2
        for ci, (heading, key) in enumerate(RANGES):
            cx = cx0 + ci * (COL_W + COL_GAP)
            s.append(text(cx, cols_y, heading, None, 11, cls="mut"))
            for ri, tr in enumerate(tops.get(key, [])):
                y = cols_y + 18 + ri * ROW_H
                s.append(_art(tr.get("art"), cx, y, ART))
                s.append(text(cx + ART + 12, y + 15, tr["title"][:24], None, 12, cls="lit"))
                s.append(text(cx + ART + 12, y + 30, tr["artist"][:26], None, 11, cls="mut"))
    return "\n".join(s) + "\n</svg>"


def music_mobile(data: dict | None) -> str:
    """The desktop player reflowed into one album-art list per time range."""
    w, cols = 390, 16
    cell_w, cell_h, gap_x, gap_y = 17, 8, 5, 4
    led_x, led_y = 20, 24
    tops = (data or {}).get("tops") or {}

    sections = []
    label_y = 290
    for heading, key in RANGES:
        tracks = tops.get(key, [])[:3]
        if not tracks:
            continue
        base_y = label_y + 14
        sections.append((heading, tracks, label_y, base_y))
        label_y = base_y + len(tracks) * 64 + 18
    height = max(282, label_y - 14)

    s = [svg_open(w, height), SCREEN_STYLE]
    s.append(f'<rect width="{w}" height="{height}" rx="10" class="bg"/>')

    # Same deterministic pixel equalizer as desktop, at half the columns.
    for c in range(cols):
        seq = _levels(c)
        x = led_x + c * (cell_w + gap_x)
        dur = round(1.5 + (c % 5) * 0.17, 2)
        for r in range(ROWS):
            y = led_y + (ROWS - 1 - r) * (cell_h + gap_y)
            vals = ";".join("1" if level > r else "0.14" for level in seq)
            s.append(
                f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" rx="1.5" '
                f'class="lit" opacity="0.14"><animate attributeName="opacity" '
                f'values="{vals}" dur="{dur}s" calcMode="discrete" '
                f'repeatCount="indefinite"/></rect>'
            )

    now = (data or {}).get("now")
    if now:
        title, artist = now["title"], now["artist"]
        pct, label, art = now["pct"], now["label"], now.get("art")
        quirk = "you may now appreciate my taste in music"
    else:
        title, artist, pct, label, art = "— not connected —", "", 0.0, "", None
        quirk = "looks like my OAuth token expired. it does that."

    s.append(text(20, 134, now and "now playing" or "status", None, 13, cls="mut"))
    s.append(_art(art, 20, 148, 64))
    s.append(text(104, 173, title[:28], None, 17, "bold", cls="lit"))
    s.append(text(104, 197, artist[:38], None, 13, cls="mut"))
    filled = round(pct * 18)
    for i in range(18):
        s.append(f'<rect x="{104 + i * 13}" y="214" width="8" height="8" rx="1" '
                 f'class="{"lit" if i < filled else "unlit"}"/>')
    if label:
        s.append(text(338, 238, label, None, 11, cls="mut", anchor="end"))
    s.append(text(20, 258, quirk, None, 12, cls="quirk"))

    for heading, tracks, heading_y, base_y in sections:
        s.append(text(20, heading_y, heading, None, 13, cls="mut"))
        for i, track in enumerate(tracks):
            y = base_y + i * 64
            s.append(_art(track.get("art"), 20, y, 50))
            s.append(text(88, y + 21, track["title"][:32], None, 16, cls="lit"))
            s.append(text(88, y + 42, track["artist"][:38], None, 13, cls="mut"))
    return "\n".join(s) + "\n</svg>"


def fetch_spotify() -> dict | None:
    """Now playing plus top tracks across three windows. None when unconfigured."""
    import base64 as b64, json, os, urllib.parse, urllib.request

    cid = os.environ.get("SPOTIFY_CLIENT_ID")
    sec = os.environ.get("SPOTIFY_CLIENT_SECRET")
    ref = os.environ.get("SPOTIFY_REFRESH_TOKEN")
    if not (cid and sec and ref):
        return None

    def api(url, data=None, headers=None):
        req = urllib.request.Request(url, data=data, headers=headers or {})
        with urllib.request.urlopen(req, timeout=25) as r:
            body = r.read()
            return json.loads(body) if body else {}

    auth = b64.b64encode(f"{cid}:{sec}".encode()).decode()
    # Refresh tokens carry a 180 day lifetime, so this WILL fail eventually.
    # Degrade rather than raise -- otherwise one dead music credential stops
    # cluster, stack and trophies rendering too.
    try:
        tok = api(
            "https://accounts.spotify.com/api/token",
            data=urllib.parse.urlencode(
                {"grant_type": "refresh_token", "refresh_token": ref}
            ).encode(),
            headers={"Authorization": f"Basic {auth}",
                     "Content-Type": "application/x-www-form-urlencoded"},
        )
    except Exception as exc:
        print(f"::warning::Spotify token refresh failed ({exc}). "
              "Re-run .github/scripts/spotify_auth.py and update the secret.")
        out = os.environ.get("GITHUB_OUTPUT")
        if out:
            with open(out, "a", encoding="utf-8") as fh:
                fh.write("spotify=expired\n")
        return None

    if tok.get("refresh_token") and tok["refresh_token"] != ref:
        print("::warning::Spotify returned a rotated refresh token. Re-run "
              "spotify_auth.py and update SPOTIFY_REFRESH_TOKEN.")

    h = {"Authorization": f"Bearer {tok['access_token']}"}
    cache: dict[str, str] = {}

    def art(images: list) -> str | None:
        """Smallest available cover, inlined. Cached: the same album turns up
        across several windows and re-encoding it would bloat the file."""
        if not images:
            return None
        url = sorted(images, key=lambda i: i.get("width") or 999)[0]["url"]
        if url not in cache:
            try:
                with urllib.request.urlopen(url, timeout=20) as r:
                    raw = r.read()
                cache[url] = "data:image/jpeg;base64," + b64.b64encode(raw).decode()
            except Exception:
                return None
        return cache[url]

    def track(it: dict) -> dict:
        return {"title": it["name"],
                "artist": ", ".join(a["name"] for a in it["artists"]),
                "art": art(it.get("album", {}).get("images", []))}

    now = None
    try:
        cur = api("https://api.spotify.com/v1/me/player/currently-playing", headers=h)
    except Exception:
        cur = {}
    if cur.get("item"):
        it, prog = cur["item"], cur.get("progress_ms", 0)
        dur = it["duration_ms"]
        now = track(it) | {
            "pct": min(1.0, prog / dur) if dur else 0.0,
            "label": f"{prog//60000}:{prog//1000%60:02d} / {dur//60000}:{dur//1000%60:02d}",
        }
    else:
        try:
            rec = api("https://api.spotify.com/v1/me/player/recently-played?limit=1",
                      headers=h).get("items", [])
            if rec:
                now = track(rec[0]["track"]) | {"pct": 1.0, "label": "last played"}
        except Exception:
            pass

    tops: dict[str, list] = {}
    for _, key in RANGES:
        try:
            items = api(
                f"https://api.spotify.com/v1/me/top/tracks?limit=5&time_range={key}",
                headers=h).get("items", [])
            tops[key] = [track(i) for i in items]
        except Exception as exc:
            # A brand new account has no history for long_term. Not an error.
            print(f"::warning::top tracks {key} unavailable ({exc})")
            tops[key] = []

    return {"now": now, "tops": tops}


# ----------------------------------------------------------------- banner ---

BW, BH = 980, 176
BANNER_STYLE = """<style>
  .bpr{fill:#656d76}.bcmd{fill:#1a7f37}.btxt{fill:#1f2328}
  .bcur{fill:#0969da}.bchrome{fill:#d0d7de}
  @media (prefers-color-scheme: dark){
    .bpr{fill:#8b949e}.bcmd{fill:#3fb950}.btxt{fill:#e6edf3}
    .bcur{fill:#58a6ff}.bchrome{fill:#30363d}
  }
</style>"""

# (text, class, start second). Typed in sequence, so it reads as a session
# rather than four lines that happen to fade in.
BANNER_LINES = [
    ("jainal09@github:~$ whoami", "bcmd", 0.20),
    ("Software Engineer — distributed systems, event-driven backends", "btxt", 1.35),
    ("jainal09@github:~$ cat focus.txt", "bcmd", 2.85),
    ("Kafka · NATS · Kubernetes · things that stay up under load", "btxt", 4.00),
]
BX, BY, BLH, BSIZE = 40, 52, 30, 15


def banner() -> str:
    """Header terminal, typed out.

    The reveal is a clipPath whose width animates -- SMIL cannot animate text
    content, so the glyphs are all present from the start and simply uncovered
    left to right. Same result, and it degrades to fully-typed rather than
    blank if a renderer ignores the animation.
    """
    s = [svg_open(BW, BH), BANNER_STYLE]
    for i, c in enumerate(("#f85149", "#d29922", "#3fb950")):
        s.append(f'<circle cx="{BX + i * 18}" cy="24" r="5.5" fill="{c}"/>')
    s.append(f'<line x1="{BX}" y1="38" x2="{BW - BX}" y2="38" class="bchrome" '
             f'stroke="currentColor" stroke-width="1" opacity="0.5"/>')

    end = BX
    for i, (body, cls, begin) in enumerate(BANNER_LINES):
        y = BY + i * BLH
        # Generous per-character estimate: overshooting the clip just reveals
        # the whole line, while undershooting would truncate it forever.
        w = int(len(body) * BSIZE * 0.75)
        dur = round(len(body) * 0.021, 2)
        s.append(
            f'<clipPath id="t{i}"><rect x="{BX}" y="{y - BSIZE}" width="0" '
            f'height="{BSIZE + 8}">'
            f'<animate attributeName="width" from="0" to="{w}" dur="{dur}s" '
            f'begin="{begin}s" fill="freeze"/></rect></clipPath>'
        )
        s.append(
            f'<text x="{BX}" y="{y}" class="{cls}" font-size="{BSIZE}" '
            f'clip-path="url(#t{i})">{esc(body)}</text>'
        )
        if i == len(BANNER_LINES) - 1:
            end = BX + int(len(body) * BSIZE * 0.6) + 8
            last_y, last_begin = y, begin + dur

    s.append(
        f'<rect x="{end}" y="{last_y - 12}" width="9" height="16" class="bcur" '
        f'opacity="0"><animate attributeName="opacity" values="0;0;1;0;1;0;1" '
        f'keyTimes="0;{round(last_begin / (last_begin + 3), 3)};'
        f'{round((last_begin + 0.4) / (last_begin + 3), 3)};'
        f'{round((last_begin + 0.9) / (last_begin + 3), 3)};'
        f'{round((last_begin + 1.4) / (last_begin + 3), 3)};'
        f'{round((last_begin + 1.9) / (last_begin + 3), 3)};1" '
        f'dur="{round(last_begin + 3, 2)}s" repeatCount="indefinite"/></rect>'
    )
    return "\n".join(s) + "\n</svg>"


def banner_mobile() -> str:
    """The desktop terminal session, word-wrapped for the narrow canvas."""
    w, h, x = 390, 226, 18
    first_rows = (53, 79, 131, 157)
    s = [svg_open(w, h), BANNER_STYLE]
    for i, colour in enumerate(("#f85149", "#d29922", "#3fb950")):
        s.append(f'<circle cx="{x + i * 16}" cy="16" r="4.5" fill="{colour}"/>')
    s.append(f'<line x1="{x}" y1="30" x2="{w - x}" y2="30" class="bchrome" '
             f'stroke="currentColor" stroke-width="1" opacity="0.65"/>')
    row = 0
    for line_index, ((body, cls, begin), first_y) in enumerate(
            zip(BANNER_LINES, first_rows, strict=True)):
        consumed = 0
        parts = wrap(body, width=37, break_long_words=False,
                     break_on_hyphens=False)
        for part_index, part in enumerate(parts):
            y = first_y + part_index * 22
            part_begin = round(begin + consumed * 0.021, 2)
            dur = round(len(part) * 0.021, 2)
            reveal = int(len(part) * BSIZE * 0.75)
            s.append(
                f'<clipPath id="mt{row}"><rect x="{x}" y="{y - 17}" '
                f'width="0" height="22"><animate attributeName="width" '
                f'from="0" to="{reveal}" dur="{dur}s" begin="{part_begin}s" '
                f'fill="freeze"/></rect></clipPath>'
            )
            s.append(text(x, y, part, None, BSIZE, cls=cls, clip=f"mt{row}"))
            consumed += len(part) + 1  # Include the wrapped space in the cadence.
            row += 1

        if line_index == len(BANNER_LINES) - 1:
            cursor_x = x + int(len(parts[-1]) * BSIZE * 0.6) + 8
            cursor_y = first_y + (len(parts) - 1) * 22
            last_end = begin + len(body) * 0.021

    cycle = last_end + 3
    s.append(
        f'<rect x="{cursor_x}" y="{cursor_y - 15}" width="8" height="18" '
        f'class="bcur" opacity="0"><animate attributeName="opacity" '
        f'values="0;0;1;0;1;0;1" keyTimes="0;{round(last_end / cycle, 3)};'
        f'{round((last_end + 0.4) / cycle, 3)};'
        f'{round((last_end + 0.9) / cycle, 3)};'
        f'{round((last_end + 1.4) / cycle, 3)};'
        f'{round((last_end + 1.9) / cycle, 3)};1" dur="{round(cycle, 2)}s" '
        f'repeatCount="indefinite"/></rect>'
    )
    return "\n".join(s) + "\n</svg>"


# ---------------------------------------------------------- contributions ---

CONTRIB_W = 980
CELL, CGAP = 13, 4
GRID_X, GRID_Y = 58, 44

# GitHub's own contribution ramp, so the graph reads as the thing it mirrors
# rather than an approximation of it.
CONTRIB_STYLE = """<style>
  .c0{fill:#ebedf0}.c1{fill:#aceebb}.c2{fill:#4ac26b}.c3{fill:#2da44e}.c4{fill:#116329}
  .clab{fill:#59636e}.cnum{fill:#1f2328}
  @media (prefers-color-scheme: dark){
    .c0{fill:#151b23}.c1{fill:#033a16}.c2{fill:#196c2e}.c3{fill:#2ea043}.c4{fill:#56d364}
    .clab{fill:#8b949e}.cnum{fill:#e6edf3}
  }
</style>"""

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]


def _level(n: int, peak: int) -> int:
    if n <= 0:
        return 0
    # Quarters of the peak rather than fixed cutoffs, so the ramp still has
    # range whether the busiest day is 9 commits or 95.
    for i, frac in enumerate((0.06, 0.18, 0.42), start=1):
        if n <= max(1, round(peak * frac)):
            return i
    return 4


def contributions(cal: dict) -> str:
    weeks = cal["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    peak = max((d["contributionCount"] for d in days), default=0)

    # Longest and current run of consecutive active days. Trailing zeroes are
    # skipped for the current streak -- today being quiet at 04:00 UTC should
    # not read as a broken streak.
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] > 0 else 0
        longest = max(longest, run)
    current = 0
    for d in reversed(days):
        if d["contributionCount"] > 0:
            current += 1
        elif current or d is days[-1]:
            break

    height = GRID_Y + 7 * (CELL + CGAP) + 42
    s = [svg_open(CONTRIB_W, height), CONTRIB_STYLE]

    seen = set()
    for wi, w in enumerate(weeks):
        first = w["contributionDays"][0]["date"]
        mon = int(first[5:7])
        if first[8:10] <= "07" and mon not in seen:
            seen.add(mon)
            s.append(text(GRID_X + wi * (CELL + CGAP), GRID_Y - 10,
                          MONTHS[mon - 1], None, 10, cls="clab"))

    for label, row in (("Mon", 1), ("Wed", 3), ("Fri", 5)):
        s.append(text(GRID_X - 34, GRID_Y + row * (CELL + CGAP) + 11,
                      label, None, 10, cls="clab"))

    for wi, w in enumerate(weeks):
        for d in w["contributionDays"]:
            x = GRID_X + wi * (CELL + CGAP)
            y = GRID_Y + d["weekday"] * (CELL + CGAP)
            s.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" '
                     f'class="c{_level(d["contributionCount"], peak)}"/>')

    base = GRID_Y + 7 * (CELL + CGAP) + 24
    s.append(text(GRID_X, base, f'{cal["totalContributions"]:,}', None, 15, "bold", cls="cnum"))
    s.append(text(GRID_X + 58, base, "contributions in the last year", None, 12, cls="clab"))
    s.append(text(GRID_X + 300, base, f"{longest}", None, 15, "bold", cls="cnum"))
    s.append(text(GRID_X + 330, base, "day longest streak", None, 12, cls="clab"))
    s.append(text(GRID_X + 490, base, f"{current}", None, 15, "bold", cls="cnum"))
    s.append(text(GRID_X + 520, base, "day current streak", None, 12, cls="clab"))

    lx = GRID_X + 700
    s.append(text(lx, base, "less", None, 10, cls="clab"))
    for i in range(5):
        s.append(f'<rect x="{lx + 34 + i * 16}" y="{base - 10}" width="12" height="12" '
                 f'rx="2.5" class="c{i}"/>')
    s.append(text(lx + 118, base, "more", None, 10, cls="clab"))
    return "\n".join(s) + "\n</svg>"


def contributions_mobile(cal: dict) -> str:
    """The most recent 16 weeks at a touch-readable cell size."""
    weeks = cal["weeks"][-16:]
    all_days = [d for week in cal["weeks"] for d in week["contributionDays"]]
    peak = max((d["contributionCount"] for d in all_days), default=0)

    longest = run = 0
    for day in all_days:
        run = run + 1 if day["contributionCount"] > 0 else 0
        longest = max(longest, run)
    s = [svg_open(390, 250), CONTRIB_STYLE,
         '<defs><rect id="mobile-cell" width="16" height="16" rx="3"/></defs>']
    seen = set()
    for wi, week in enumerate(weeks):
        first = week["contributionDays"][0]["date"]
        month, day = int(first[5:7]), int(first[8:10])
        if (wi == 0 or day <= 7) and month not in seen:
            seen.add(month)
            s.append(text(42 + wi * 20, 24, MONTHS[month - 1], None, 12, cls="clab"))
    for label, row in (("Mon", 1), ("Wed", 3), ("Fri", 5)):
        s.append(text(4, 36 + row * 20 + 12, label, None, 11, cls="clab"))
    for wi, week in enumerate(weeks):
        for day in week["contributionDays"]:
            x, y = 42 + wi * 20, 36 + day["weekday"] * 20
            level = _level(day["contributionCount"], peak)
            s.append(f'<use href="#mobile-cell" xlink:href="#mobile-cell" '
                     f'x="{x}" y="{y}" class="c{level}"/>')

    s += [
        text(42, 207, f'{cal["totalContributions"]:,}', None, 18, "bold", cls="cnum"),
        text(105, 207, "contributions this year", None, 13, cls="clab"),
        text(42, 234, f"{longest}", None, 18, "bold", cls="cnum"),
        text(72, 234, "day longest streak", None, 13, cls="clab"),
    ]
    return "\n".join(s) + "\n</svg>"


def fetch_calendar() -> dict:
    import json, os, subprocess, urllib.request
    q = """{ user(login:"jainal09"){ contributionsCollection{ contributionCalendar{
      totalContributions weeks{ contributionDays{ date contributionCount weekday } } } } } }"""
    tok = os.environ.get("GITHUB_TOKEN") or subprocess.run(
        ["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=json.dumps({"query": q}).encode(),
        headers={"Authorization": f"bearer {tok}", "Content-Type": "application/json",
                 "User-Agent": "jainal09-profile-art"})
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    return payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    calendar = fetch_calendar()
    spotify = fetch_spotify()
    pieces = (
        ("banner", banner()), ("banner-mobile", banner_mobile()),
        ("contributions", contributions(calendar)),
        ("contributions-mobile", contributions_mobile(calendar)),
        ("cluster", cluster()), ("cluster-mobile", cluster_mobile()),
        ("stack", stack()), ("stack-mobile", stack_mobile()),
        ("trophies", trophies(fetch_stats())),
        ("music", music(spotify)), ("music-mobile", music_mobile(spotify)),
    )
    for name, body in pieces:
        path = OUT_DIR / f"{name}.svg"
        path.write_text(body, encoding="utf-8")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
