"""Scope: Authenticate a human in Cognito using in-memory PKCE and a loopback callback."""

import base64
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import secrets
import time
from urllib.parse import parse_qs, urlencode, urlsplit
import webbrowser

from cnc_http_client import CncHttpClient


class CncLoginCallback(BaseHTTPRequestHandler):
    def do_GET(self):
        login = self.server.login
        parsed = urlsplit(self.path)
        values = parse_qs(parsed.query)
        valid = (len(self.path) <= 4096 and self.headers.get("Host") == "localhost:8766"
                 and parsed.path == "/callback" and len(values.get("state", [])) == 1
                 and secrets.compare_digest(values["state"][0].encode(), login.state.encode()))
        if not valid:
            self.send_error(400, "Invalid sign-in callback")
            return
        login.code = values["code"][0] if len(values.get("code", [])) == 1 else ""
        login.finished = True
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        self.wfile.write(b"Sign-in received. Return to your AIkea viewer." if login.code else b"Sign-in cancelled. Return to AIkea and retry.")

    def log_message(self, format, *args):
        # OAuth authorization codes and state must never enter request logs.
        pass


class CncBrowserLogin:
    CALLBACK = "http://localhost:8766/callback"

    def __init__(self, login_url, client_id, http=None):
        self.login_url, self.client_id = login_url, client_id
        self.http = http or CncHttpClient()
        self.code, self.finished = "", False

    def authenticate(self):
        self.code, self.finished = "", False
        self.state, verifier = secrets.token_urlsafe(32), secrets.token_urlsafe(64)
        challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")
        query = urlencode({"response_type": "code", "client_id": self.client_id, "redirect_uri": self.CALLBACK,
                           "scope": "openid email aikea/submit", "state": self.state,
                           "code_challenge": challenge, "code_challenge_method": "S256"})
        with HTTPServer(("127.0.0.1", 8766), CncLoginCallback) as server:
            server.login, server.timeout = self, 1
            if not webbrowser.open(self.login_url + "/oauth2/authorize?" + query):
                raise ValueError("Could not open sign-in in your browser. Open AIkea on a desktop with a browser.")
            deadline = time.monotonic() + 300
            while not self.finished and time.monotonic() < deadline:
                server.handle_request()
        if not self.code:
            raise ValueError("Sign-in was cancelled or timed out. Retry to sign in.")
        body = urlencode({"grant_type": "authorization_code", "client_id": self.client_id, "redirect_uri": self.CALLBACK,
                          "code": self.code, "code_verifier": verifier}).encode()
        result = json.loads(self.http.post(self.login_url + "/oauth2/token", body,
                                          {"Content-Type": "application/x-www-form-urlencoded"}))
        self.code = ""
        return result["access_token"]
