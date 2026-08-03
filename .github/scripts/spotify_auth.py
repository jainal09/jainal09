#!/usr/bin/env python3
"""One-time helper: turn a Spotify app into a refresh token.

Run this on your own machine. It opens Spotify in your browser, you log in
there, and it prints a refresh token to paste into GitHub repo secrets. The
token is long-lived, so this is a one-off.

    export SPOTIFY_CLIENT_ID=...
    export SPOTIFY_CLIENT_SECRET=...
    python3 .github/scripts/spotify_auth.py

Nothing is written to disk and the client secret is never printed. The
refresh token IS printed -- that is the point -- so run it somewhere your
terminal scrollback is not being shared.
"""

from __future__ import annotations

import base64
import http.server
import json
import os
import secrets
import sys
import threading
import urllib.parse
import urllib.request
import webbrowser

PORT = 8888
REDIRECT = f"http://127.0.0.1:{PORT}/callback"
SCOPES = "user-read-currently-playing user-read-recently-played"

_code: str | None = None
_state_sent = secrets.token_urlsafe(16)


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        global _code
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        ok = q.get("state", [""])[0] == _state_sent and "code" in q
        if ok:
            _code = q["code"][0]
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            b"Authorised. You can close this tab and return to the terminal."
            if ok else b"Mismatch or denied. Nothing was captured; try again."
        )

    def log_message(self, *_):  # keep the terminal clean
        pass


def main() -> None:
    cid = os.environ.get("SPOTIFY_CLIENT_ID")
    sec = os.environ.get("SPOTIFY_CLIENT_SECRET")
    if not (cid and sec):
        sys.exit("Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET first.")

    url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(
        {"client_id": cid, "response_type": "code", "redirect_uri": REDIRECT,
         "scope": SCOPES, "state": _state_sent}
    )

    server = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()

    print(f"\nRedirect URI registered on the Spotify app must be exactly:\n  {REDIRECT}\n")
    # Always print the URL. webbrowser.open() silently no-ops when there is no
    # session to open into -- launched from a daemon, over ssh, from CI -- and
    # without the URL there is nothing to fall back to.
    print("Open this if your browser does not appear:\n")
    print(f"  {url}\n", flush=True)
    try:
        webbrowser.open(url)
    except Exception:
        pass

    while _code is None:
        server.handle_request()
    server.shutdown()

    auth = base64.b64encode(f"{cid}:{sec}".encode()).decode()
    req = urllib.request.Request(
        "https://accounts.spotify.com/api/token",
        data=urllib.parse.urlencode(
            {"grant_type": "authorization_code", "code": _code, "redirect_uri": REDIRECT}
        ).encode(),
        headers={"Authorization": f"Basic {auth}",
                 "Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        tok = json.load(r)

    refresh = tok.get("refresh_token")
    if not refresh:
        sys.exit(f"No refresh token returned: {tok}")

    print("\n" + "=" * 62)
    print("SPOTIFY_REFRESH_TOKEN")
    print(refresh)
    print("=" * 62)
    print("\nAdd it, plus the client id and secret, at:")
    print("  Settings -> Secrets and variables -> Actions -> New repository secret")
    print("  SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET / SPOTIFY_REFRESH_TOKEN\n")


if __name__ == "__main__":
    main()
