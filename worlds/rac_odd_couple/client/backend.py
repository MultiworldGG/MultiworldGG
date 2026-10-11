"""
Minimal static-file + button-gating relay server for the Odd Couple frontend.

No Archipelago protocol client runs in this process - the browser page
(frontend/app.js) talks to the AP server directly via archipelago.min.js.
This process only serves the frontend/patched-swf as static files and
answers the patched swf's own LoadVars button-gating calls (see
swf_patch.py): a SWF's ActionScript can only reach out over plain HTTP, it
has no way to call into the page's JS directly. The frontend keeps this
server's suppressed-event state in sync via POST /api/suppressed after every
item update, and polls GET /api/poll-received to learn about scene-initiated
events the swf reported, since there's no push channel (websocket) here. It
also tracks whether the browser tab is still open (via a heartbeat the page
pings on an interval, plus an immediate beacon on tab close) so the process
can exit on its own once the page is gone instead of lingering forever.
"""
from __future__ import annotations

import json
import logging
import os
import shutil
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Optional
from urllib.parse import parse_qs, urlparse

import Utils

logger = logging.getLogger("OddCoupleServer")

HOST = "127.0.0.1"
HTTP_PORT = 8000
BASE_URL = f"http://{HOST}:{HTTP_PORT}"

# How long without a heartbeat before we assume the tab is gone (crashed,
# force-quit, lost network) and shut down. Generous, since backgrounded tabs
# get their JS timers throttled by the browser and may go quiet for a while
# without actually having been closed - the normal "user closed the tab"
# case is handled instantly via the /api/closed beacon instead.
HEARTBEAT_TIMEOUT_SECONDS = 90

ALL_SCENES = ["stereo", "taxiDriver", "gimp", "phonecall1", "scissors", "tv"]

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
PATCHED_SWF_NAME = "ap_patched_odd_couple.swf"

_CONTENT_TYPES = {
    ".html": "text/html",
    ".js": "application/javascript",
    ".css": "text/css",
}


def runtime_game_dir() -> str:
    """Writable folder where the patched swf is installed - independent of
    any external project, so this world has no runtime dependency on one."""
    path = Utils.user_path("rac_odd_couple")
    os.makedirs(path, exist_ok=True)
    return path


def install_patched_swf(patched_swf_path: str) -> str:
    """Copy the freshly patched swf (built by Patch.create_rom_file from the
    .apoddcouple file) into our runtime folder, under a fixed name the
    frontend always requests."""
    dest = os.path.join(runtime_game_dir(), PATCHED_SWF_NAME)
    shutil.copyfile(patched_swf_path, dest)
    return PATCHED_SWF_NAME


def find_installed_patched_swf() -> Optional[str]:
    """Return PATCHED_SWF_NAME if a previous run already installed it, so a
    client-only launch (no .apoddcouple this time) still has a movie to
    serve instead of leaving the frontend with nothing to load."""
    if os.path.exists(os.path.join(runtime_game_dir(), PATCHED_SWF_NAME)):
        return PATCHED_SWF_NAME
    return None


class OddCoupleServer:
    """Bare stdlib HTTP server bridging the browser-side SWF player's own
    LoadVars calls to in-memory state the browser page keeps synced. Holds no
    Archipelago connection itself - the browser page owns that directly via
    archipelago.min.js."""

    def __init__(self) -> None:
        self.suppressed_events: "set[str]" = set(ALL_SCENES)
        self._pending_received: "list[str]" = []
        self._lock = threading.Lock()
        self._http_server: Optional[ThreadingHTTPServer] = None
        self._http_thread: Optional[threading.Thread] = None
        self._watchdog_thread: Optional[threading.Thread] = None
        self._last_heartbeat: Optional[float] = None
        self.page_closed = threading.Event()

    def start(self) -> None:
        server_ref = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, fmt: str, *args: object) -> None:
                logger.debug("%s - %s", self.address_string(), fmt % args)

            def _send_json(self, status: int, payload: object) -> None:
                body = json.dumps(payload).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def _send_text(self, status: int, text: str) -> None:
                body = text.encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def _send_file(self, path: str, content_type: str) -> None:
                if not os.path.isfile(path):
                    self._send_text(404, "Not found")
                    return
                with open(path, "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def _send_package_file(self, path: str, content_type: str) -> None:
                # Frontend assets ship inside this world's package, which may be a
                # real directory (dev checkout) or a zipimport-loaded .apworld - a
                # plain open() can't read the latter, since __file__ there is a
                # virtual path into the zip. __loader__.get_data() uses the same
                # path convention __file__ does and works for both cases.
                try:
                    data = __loader__.get_data(path)
                except OSError:
                    self._send_text(404, "Not found")
                    return
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
                parsed = urlparse(self.path)
                path, query = parsed.path, parse_qs(parsed.query)

                if path == "/api/status":
                    self._send_json(200, {"swf_installed": find_installed_patched_swf() is not None})
                    return

                if path == "/api/heartbeat":
                    with server_ref._lock:
                        server_ref._last_heartbeat = time.monotonic()
                    self._send_text(200, "ok")
                    return

                if path == "/api/check":
                    scene = (query.get("scene") or [""])[0]
                    with server_ref._lock:
                        allowed = scene not in server_ref.suppressed_events
                    self._send_text(200 if allowed else 403, "ok" if allowed else "suppressed")
                    return

                if path == "/api/received":
                    scene = (query.get("scene") or [""])[0]
                    with server_ref._lock:
                        server_ref._pending_received.append(scene)
                    self._send_text(200, "ok")
                    return

                if path == "/api/poll-received":
                    with server_ref._lock:
                        pending, server_ref._pending_received = server_ref._pending_received, []
                    self._send_json(200, pending)
                    return

                if path == f"/game/{PATCHED_SWF_NAME}":
                    self._send_file(os.path.join(runtime_game_dir(), PATCHED_SWF_NAME),
                                    "application/x-shockwave-flash")
                    return

                rel = path.lstrip("/") or "index.html"
                content_type = _CONTENT_TYPES.get(os.path.splitext(rel)[1], "application/octet-stream")
                self._send_package_file(os.path.join(FRONTEND_DIR, rel), content_type)

            def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length) if length else b"{}"
                try:
                    payload = json.loads(raw)
                except json.JSONDecodeError:
                    payload = {}

                if self.path == "/api/suppressed":
                    with server_ref._lock:
                        server_ref.suppressed_events = set(payload.get("events", []))
                    self._send_text(200, "ok")
                    return

                if self.path == "/api/closed":
                    # navigator.sendBeacon() fires this on tab close/refresh - the
                    # immediate signal; the heartbeat watchdog below is only the
                    # fallback for a crashed/force-quit browser.
                    logger.info("Browser tab closed - shutting down.")
                    server_ref.page_closed.set()
                    self._send_text(200, "ok")
                    return

                self._send_text(404, "Not found")

        self._http_server = ThreadingHTTPServer((HOST, HTTP_PORT), Handler)
        self._http_thread = threading.Thread(target=self._http_server.serve_forever, daemon=True)
        self._http_thread.start()

        self._watchdog_thread = threading.Thread(target=self._watchdog, daemon=True)
        self._watchdog_thread.start()

    def _watchdog(self) -> None:
        # No timeout starts ticking until the page's first heartbeat arrives,
        # so a slow-loading (or never-loaded) browser doesn't get flagged as
        # "closed" before it's even had a chance to open.
        while not self.page_closed.wait(2):
            with self._lock:
                last_heartbeat = self._last_heartbeat
            if last_heartbeat is not None and time.monotonic() - last_heartbeat > HEARTBEAT_TIMEOUT_SECONDS:
                logger.warning(f"No heartbeat from the browser tab in over {HEARTBEAT_TIMEOUT_SECONDS}s - "
                               "assuming it's gone. Shutting down.")
                self.page_closed.set()
                return

    def stop(self) -> None:
        logger.info("Stopping the Odd Couple relay server.")
        self.page_closed.set()
        if self._http_server:
            self._http_server.shutdown()
