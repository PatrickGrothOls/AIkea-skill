"""Scope: Send bounded HTTPS requests without redirecting credentials or upload grants."""

import json
from urllib.request import HTTPRedirectHandler, Request, build_opener


class NoCncRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class CncHttpClient:
    def __init__(self):
        self.opener = build_opener(NoCncRedirects())

    def post(self, url, data, headers):
        with self.opener.open(Request(url, data=data, headers=headers, method="POST"), timeout=120) as response:
            content = response.read(65_537)
        if len(content) > 65_536:
            raise ValueError("Intake response exceeds limit.")
        return content

    def json(self, url, body, token):
        return json.loads(self.post(url, json.dumps(body).encode(), {
            "Content-Type": "application/json", "Authorization": "Bearer " + token}))
