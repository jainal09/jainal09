#!/usr/bin/env python3
"""Render the profile banner: an animated NATS-style cluster.

Not a stats card. The numbers on it come from work that actually happened --
the throughput knack measured, the releases the upstream fixes shipped in --
rather than from counting repositories.

One file, not two. The background is transparent and every colour is chosen
to hold up on both GitHub themes, so there is no prefers-color-scheme swap to
go wrong. That failure mode is invisible to whoever is hitting it.
"""

from __future__ import annotations

from pathlib import Path

OUT = Path("assets/cluster.svg")

W, H = 980, 300

# Colours that read on #0d1117 and on #ffffff alike. Nothing near-white,
# nothing near-black; mid-tones only.
GREEN = "#3fb950"
BLUE = "#4c8eda"
DIM = "#7d8590"
EDGE = "#8b949e"

PUBS = [(70, 80), (70, 220)]
CORE = [(330, 70), (330, 230), (470, 150)]
SUBS = [(850, 80), (850, 220)]

# (from, to, delay) -- delays stagger the packets so the mesh looks alive
# rather than metronomic.
FLOWS = [
    (PUBS[0], CORE[0], 0.0),
    (PUBS[1], CORE[1], 1.1),
    (CORE[0], CORE[2], 0.4),
    (CORE[1], CORE[2], 1.5),
    (CORE[0], CORE[1], 2.1),
    (CORE[2], SUBS[0], 0.9),
    (CORE[2], SUBS[1], 1.9),
]

LINKS = [
    (PUBS[0], CORE[0]), (PUBS[1], CORE[1]),
    (CORE[0], CORE[1]), (CORE[0], CORE[2]), (CORE[1], CORE[2]),
    (CORE[2], SUBS[0]), (CORE[2], SUBS[1]),
]


def main() -> None:
    mono = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
    s = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="{mono}" fill="none">'
    ]

    # static links
    for (x1, y1), (x2, y2) in LINKS:
        s.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{EDGE}" '
            f'stroke-width="1" opacity="0.35"/>'
        )

    # motion paths + the packets riding them
    for i, ((x1, y1), (x2, y2), delay) in enumerate(FLOWS):
        s.append(f'<path id="f{i}" d="M{x1},{y1} L{x2},{y2}" stroke="none"/>')
        s.append(
            f'<circle r="3.5" fill="{GREEN}">'
            f'<animateMotion dur="2.4s" begin="{delay}s" repeatCount="indefinite" '
            f'keyPoints="0;1" keyTimes="0;1" calcMode="linear">'
            f'<mpath href="#f{i}" xlink:href="#f{i}"/></animateMotion>'
            f'<animate attributeName="opacity" values="0;1;1;0" dur="2.4s" '
            f'begin="{delay}s" repeatCount="indefinite"/></circle>'
        )

    # endpoints
    for x, y in PUBS + SUBS:
        s.append(f'<circle cx="{x}" cy="{y}" r="7" stroke="{BLUE}" stroke-width="2"/>')

    # cluster nodes, breathing slightly out of phase
    for i, (x, y) in enumerate(CORE):
        s.append(
            f'<circle cx="{x}" cy="{y}" r="11" stroke="{GREEN}" stroke-width="2">'
            f'<animate attributeName="r" values="11;13;11" dur="3s" '
            f'begin="{i * 0.7}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="1;0.55;1" dur="3s" '
            f'begin="{i * 0.7}s" repeatCount="indefinite"/></circle>'
        )

    # Everything is left-anchored at an explicit x. text-anchor="end"/"middle"
    # would be tidier, but it puts the right edge of the string at the mercy of
    # whichever monospace face the viewer resolves -- and anything that overruns
    # here is clipped by the viewBox rather than just looking loose.
    def text(x, y, body, fill=DIM, size=13, weight="normal"):
        s.append(
            f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" '
            f'font-weight="{weight}">{body}</text>'
        )

    text(52, 30, "publishers", DIM, 11)
    text(360, 30, "cluster", GREEN, 11)
    text(780, 30, "subscribers", DIM, 11)

    text(52, 272, "5.0M msg/s", GREEN, 15, "bold")
    text(160, 272, "measured by knack on constrained hardware", DIM, 12)
    text(520, 272, "shipped: nats-server 2.14.4 · nui 0.9.3", BLUE, 12)

    s.append("</svg>")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(s), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
