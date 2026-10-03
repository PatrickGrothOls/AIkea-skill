"""Scope: Verify real loopback OAuth state rejection and PKCE token exchange."""

import base64
import hashlib
from http.client import HTTPConnection
import json
from threading import Thread
from urllib.parse import parse_qs, urlsplit, urlencode

from cnc_browser_login import CncBrowserLogin
from cnc_http_client import NoCncRedirects


class LoginTransport:
    def __init__(self):
        self.form = None

    def post(self, url, body, headers):
        self.form = parse_qs(body.decode())
        return json.dumps({"access_token": "synthetic", "refresh_token": "must-not-be-retained"}).encode()


class TestCncBrowserLogin:
    def open_browser(self, url):
        self.query = parse_qs(urlsplit(url).query)
        self.thread = Thread(target=self.callback)
        self.thread.start()
        return True

    def callback(self):
        self.statuses = []
        for state in ["forged-state", self.query["state"][0]]:
            connection = HTTPConnection("127.0.0.1", 8766, timeout=5)
            path = "/callback?" + urlencode({"state": state, "code": "synthetic-code"})
            connection.request("GET", path, headers={"Host": "localhost:8766"})
            response = connection.getresponse()
            self.statuses.append(response.status)
            response.read()
            connection.close()

    def test_state_and_pkce_flow(self, monkeypatch):
        monkeypatch.setattr("cnc_browser_login.webbrowser.open", self.open_browser)
        transport = LoginTransport()
        login = CncBrowserLogin("https://example.invalid", "client", transport)
        assert login.authenticate() == "synthetic"
        self.thread.join(timeout=5)
        assert self.statuses == [400, 200]
        verifier = transport.form["code_verifier"][0]
        expected = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")
        assert self.query["code_challenge"] == [expected]
        assert transport.form["code"] == ["synthetic-code"]
        assert login.code == "" and not hasattr(login, "refresh_token")

    def test_redirects_cannot_forward_credentials(self):
        assert NoCncRedirects().redirect_request(None, None, 307, "redirect", {}, "https://attacker.invalid") is None
