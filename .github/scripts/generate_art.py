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


def esc(s: str) -> str:
    """XML-escape. Every string here is escaped at the single point it becomes
    markup, rather than at each call site -- track and artist names are the one
    input I do not control, and a bare & in "Jonathan & Friends" does not
    degrade, it makes the whole file unparseable.
    """
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def text(x, y, body, fill=DIM, size=13, weight="normal", cls=None) -> str:
    # Left-anchored at an explicit x throughout. text-anchor="end" puts the
    # right edge of the string at the mercy of whichever monospace face the
    # viewer resolves, and an overrun here is clipped by the viewBox.
    return (
        f'<text x="{x}" y="{y}"'
        + (f' class="{cls}"' if cls else f' fill="{fill}"')
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


# --------------------------------------------------------------- worldmap ---

# Land mask rasterised from Natural Earth ne_110m_land (public domain), not
# traced from anyone's artwork. '#' is land, '.' is water.
LANDMASK = """....................##........#..#####...#####################...............#...................................##...................................
.......................#......#.#####.........################................................#............##########.................................
..................##.#####..###..#####.........#############................................##.....##...####################.....###..................
..#######.............######..##..########.....#############...................####...............#######################################.............
.#####################...##..####.##..#.###.....#########....................##########..#.##########.############################################....
##################################.....###.#....######......####...........#####.####..###########################################################....
..##############################..#.#...###......####.....................#####.#################################################################.....
.##############################.......##..........##.....................#####.#########################################################.#.####.......
...###......###################.......###..#.............................#.###..##################################################....#..##...........
....#..........##################.....#######.......................#.....#.#..#################################################........###...........
.#..............####################.#########.....................#.#....#..#.#################################################........##............
.................###################.##########...................##.##.##########################################################......#.............
.................#########################....#........................##########################################################.#...................
..................#########################...##.....................############################################################.....................
..................###########################.........................#############.#.##########################################......................
..................#######################..........................######..#.#####.....########################################...#...................
..................######################...........................####.....#..###.###.######################################....#....................
...................####################...........................####.......#.#..######################################...#.....#....................
...................####################.............................#..####.......#######################################..##...#.....................
....................##################..............................#######..........####################################..#.###......................
.....................################.............................###########..#.....####################################....#........................
.......................##########..#..............................#######################################################.............................
......................#.######......#............................###################.######.#############################.............................
.......................#.#####......#...........................#####################.#####....#########################..............................
........................#.###...................................#####################..########....####################...............................
..........................####...#....#........................#######################.########.....#######..######.#.................................
...........................###..##......##......................######################..######.......#####....#####.#.................................
.............................####..............................########################.#####........####.....#####......#............................
................................####...........................############################...........##.......#####..................................
..................................#.....#......................##########################.............##.........###..................................
...................................#...#.####...................############################..........##..........#...................................
....................................#.########...................##########################.............#.................#...........................
......................................##########..................####...##################...................#.##.....#..............................
......................................###########.........................################.....................#.#....##..............................
.....................................############.........................###############.......................#...####.##...........................
....................................###############.......................##############........................##..###.##...##.......................
.....................................#################.....................############..........................##...#.##.#..#####...................
....................................####################...................############...........................#.............####.#................
.....................................###################....................###########..............................##.........####..................
......................................#################.....................###########...............................................................
......................................#################.....................###########......................................###......................
.......................................###############.....................############...#................................#.##...#...................
........................................##############.....................############..##...............................##########..................
.........................................#############......................#########....##..............................###########..................
.........................................############.......................#########....##............................##############.................
.........................................###########........................#########....#............................################................
.........................................#########...........................#######..................................#################...............
.........................................#########...........................#######..................................#################...............
........................................#########.............................#####....................................################...............
........................................########..............................####.....................................####....#######................
........................................######.#.......................................................................#........######................
........................................#######..................................................................................####..........#......
........................................####...................................................................................................##.....
.......................................####........................................................................................##.........#.......
........................................###..................................................................................................##.......
.......................................###..................................................................................................##........
.......................................####...........................................................................................................
.......................................###............................................................................................................
.......................................###............................................................................................................
........................................###..........................................................................................................."""

MAP_LON0, MAP_LON1, MAP_LAT0, MAP_LAT1 = -168, 190, 78, -56
MAP_W, MAP_H = 980, 260
MAP_PAD, DOT = 18, 3

MAP_STYLE = """<style>
  .land{fill:#d0d7de}.node{fill:#1a7f37}.arc{stroke:#0969da}
  .pulse{fill:#0969da}.mtxt{fill:#656d76}.mname{fill:#1f2328}
  @media (prefers-color-scheme: dark){
    .land{fill:#30363d}.node{fill:#3fb950}.arc{stroke:#58a6ff}
    .pulse{fill:#58a6ff}.mtxt{fill:#8b949e}.mname{fill:#e6edf3}
  }
</style>"""

# Somewhere I have lived, studied, or shipped to.
PLACES = [
    ("Boston", -71.06, 42.36),
    ("London", -0.13, 51.51),
    ("Mumbai", 72.88, 19.08),
    ("Singapore", 103.82, 1.35),
    ("Sydney", 151.21, -33.87),
]
HOPS = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 2)]


def _project(lon: float, lat: float) -> tuple[float, float]:
    gx = (lon - MAP_LON0) / (MAP_LON1 - MAP_LON0)
    gy = (lat - MAP_LAT0) / (MAP_LAT1 - MAP_LAT0)
    return (MAP_PAD + gx * (MAP_W - 2 * MAP_PAD),
            MAP_PAD + gy * (MAP_H - 2 * MAP_PAD))


def worldmap() -> str:
    rows = LANDMASK.splitlines()
    nrows, ncols = len(rows), len(rows[0])
    cw = (MAP_W - 2 * MAP_PAD) / ncols
    ch = (MAP_H - 2 * MAP_PAD) / nrows

    s = [svg_open(MAP_W, MAP_H), MAP_STYLE]

    # Every land cell in a single <path>. As individual <circle> elements this
    # is ~2800 nodes and six figures of bytes; as one path of square subpaths
    # it is a fraction of that, and they all share a colour anyway.
    d = []
    for r, row in enumerate(rows):
        y = round(MAP_PAD + r * ch, 1)
        for c, ch_ in enumerate(row):
            if ch_ == "#":
                d.append(f"M{round(MAP_PAD + c * cw, 1)} {y}h{DOT}v{DOT}h-{DOT}z")
    s.append(f'<path class="land" d="{"".join(d)}"/>')

    pts = [_project(lon, lat) for _, lon, lat in PLACES]

    for i, (a, b) in enumerate(HOPS):
        (x1, y1), (x2, y2) = pts[a], pts[b]
        # Bow the link upward so overlapping routes stay legible.
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - abs(x2 - x1) * 0.18
        s.append(f'<path id="hop{i}" class="arc" fill="none" stroke-width="1" '
                 f'opacity="0.35" d="M{x1:.1f} {y1:.1f} Q{mx:.1f} {my:.1f} {x2:.1f} {y2:.1f}"/>')
        s.append(
            f'<circle r="3" class="pulse">'
            f'<animateMotion dur="3.2s" begin="{round(i * 0.55, 2)}s" '
            f'repeatCount="indefinite" calcMode="linear">'
            f'<mpath href="#hop{i}" xlink:href="#hop{i}"/></animateMotion>'
            f'<animate attributeName="opacity" values="0;1;1;0" dur="3.2s" '
            f'begin="{round(i * 0.55, 2)}s" repeatCount="indefinite"/></circle>'
        )

    for i, ((name, _, _), (x, y)) in enumerate(zip(PLACES, pts)):
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" class="node">'
                 f'<animate attributeName="r" values="3.5;5.5;3.5" dur="2.6s" '
                 f'begin="{round(i * 0.5, 2)}s" repeatCount="indefinite"/></circle>')

    s.append(text(MAP_PAD + 4, MAP_H - 14, "jainal09", None, 15, "bold", cls="mname"))
    s.append(text(MAP_PAD + 92, MAP_H - 14,
                  "distributed systems · event-driven backends · platform",
                  None, 12, cls="mtxt"))
    return "\n".join(s) + "\n</svg>"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pieces = (("banner", banner()), ("worldmap", worldmap()), ("cluster", cluster()), ("stack", stack()),
              ("trophies", trophies(fetch_stats())), ("music", music(fetch_spotify())))
    for name, body in pieces:
        path = OUT_DIR / f"{name}.svg"
        path.write_text(body, encoding="utf-8")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
