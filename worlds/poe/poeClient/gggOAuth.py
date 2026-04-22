import logging
import os
import pkgutil
import sys
from worlds.poe.poeClient import fileHelper
fileHelper.load_vendor_modules()
import http.server
import socketserver
import urllib.parse
import webbrowser
import base64
import hashlib
import requests
import asyncio
import httpx
import time

# === CONFIG ===
CLIENT_ID = "archipelagopoe"
REDIRECT_URI = "http://127.0.0.1:8234/oauth-callback"
SCOPES = "account:profile account:characters account:stashes account:leagues"
PORT = 8234
logger = logging.getLogger("poeClient.gggOAuth")

# === Step 1: Generate PKCE pair ===
_code_verifier = base64.urlsafe_b64encode(os.urandom(64)).rstrip(b'=').decode()
_code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(_code_verifier.encode()).digest()
).rstrip(b'=').decode()

# === Step 2: Build Auth URL ===
_params = {
    "response_type": "code",
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPES,
    "state": "mystate",
    "code_challenge": _code_challenge,
    "code_challenge_method": "S256",
}
_auth_url = f"https://www.pathofexile.com/oauth/authorize?{urllib.parse.urlencode(_params)}"
access_token = ""
token_expire_time = None
slot_info = {}  # Set externally before calling async_oauth_login to pass server/slot/password to tracker

TRACKER_BASE_URL = "https://stubobis1.github.io/pathofexile_ap/"
# === Step 3: Start local callback server ===


#create a lock for async_oauth_login
_oauth_lock = asyncio.Lock()

async def async_oauth_login() -> dict:
    """
    Async version of oauth_login. Returns a new access_token.
    """

    async with _oauth_lock:
        code_future = asyncio.get_event_loop().create_future()

        class AsyncOAuthHandler(http.server.SimpleHTTPRequestHandler):
            global access_token, token_expire_time

            def do_GET(self):
                parsed = urllib.parse.urlparse(self.path)
                if parsed.path == "/oauth-callback":
                    params = urllib.parse.parse_qs(parsed.query)
                    code = params.get("code", [None])[0]
                    if code:
                        self.send_response(200)
                        self.send_header("Content-Type", "text/html; charset=utf-8")
                        self.end_headers()
                        html_bytes = pkgutil.get_data("worlds.poe.poeClient", "static/oauth_success.html")
                        html = html_bytes.decode("utf-8")
                        # Build tracker redirect URL with slot info as query params
                        params = {k: v for k, v in slot_info.items() if v}
                        params["autoconnect"] = "1"
                        redirect_url = TRACKER_BASE_URL + "?" + urllib.parse.urlencode(params)
                        html = html.replace(
                            "url=https://stubobis1.github.io/pathofexile_ap/",
                            f"url={redirect_url}"
                        )
                        self.wfile.write(html.encode("utf-8"))
                        if not code_future.done():
                            code_future.set_result(code)
                        def shutdown_server(server):
                            server.shutdown()
                        import threading
                        threading.Thread(target=shutdown_server, args=(self.server,), daemon=True).start()
                    else:
                        self.send_response(400)
                        self.send_header("Content-Type", "text/html; charset=utf-8")
                        self.end_headers()
                        error_bytes = pkgutil.get_data("worlds.poe.poeClient", "static/oauth_error.html")
                        self.wfile.write(error_bytes)


        logger.info(f"🔊 Listening for callback on {REDIRECT_URI} ...")
        try:
            server = socketserver.TCPServer(("", PORT), AsyncOAuthHandler)
        except Exception as e:
            await asyncio.sleep(10)
            logger.error(f"Failed to start local server on port {PORT}: {e}")
            raise e
        webbrowser.open(_auth_url)
        loop = asyncio.get_event_loop()
        executor_future = loop.run_in_executor(None, server.serve_forever)
        try:
            await executor_future
        except asyncio.CancelledError:
            server.shutdown()
            raise
        code = await code_future

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://www.pathofexile.com/oauth/token",
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": REDIRECT_URI,
                    "client_id": CLIENT_ID,
                    "code_verifier": _code_verifier,
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": "Archipelago-PoE",
                },
            )
            resp.raise_for_status()
            tokens = resp.json()
            token_expire_time = tokens["expires_in"] + time.time()
            access_token = tokens["access_token"]
            logger.info("\n✅ Access Token:" + tokens["access_token"])
            logger.info(f"⏳ Token expires at:{token_expire_time} seconds since epoch, or {token_expire_time - time.time()} seconds from now")

            # return a dict with expire time and access token
            return {
                "access_token": access_token,
                "expires_at": token_expire_time
            }




if __name__ == '__main__':
    # Run the async OAuth login (fixes DeprecationWarning)
    logger.setLevel(logging.DEBUG)
    result = asyncio.run(async_oauth_login())
    logger.info(f"OAuth login result:  -------->       {result['access_token']}      <-------- expires at {result['expires_at']} seconds since epoch")


## === Step 5: Launch browser and serve ===
#def oauth_login():
#
#    logger.info(f"🌐 Opening browser to log in...")
#    webbrowser.open(_auth_url)
#
#    logger.info(f"🔊 Listening for callback on {REDIRECT_URI} ...")
#    with socketserver.TCPServer(("", PORT), OAuthHandler) as httpd:
#        httpd.serve_forever()
#
#
#if __name__ == '__main__':
#    oauth_login()