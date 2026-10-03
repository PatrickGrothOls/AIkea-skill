"""Scope: Submit one frozen viewer package through hosted intake without AWS credentials."""

import hashlib
import json
import re
import secrets
from urllib.error import HTTPError, URLError

from cnc_deployment_config import CncDeploymentConfig
from cnc_browser_login import CncBrowserLogin
from cnc_http_client import CncHttpClient
from quote_object_store import QuoteDeliveryError
from quote_submission_session import QuoteSubmissionSession


class HostedQuoteSession(QuoteSubmissionSession):
    def __init__(self, package, model_sha256, config, http=None, login=None):
        super().__init__(package, model_sha256)
        self.api, self.login_url, client_id = config["GatewayUrl"], config["LoginUrl"], config["ClientId"]
        account, region = config["AccountId"], config["Region"]
        CncDeploymentConfig.validate_identity(account, region)
        self.region = region
        self.quarantine_bucket = f"aikea-cnc-intake-{account}-{region}"
        if (not re.fullmatch(r"https://[a-z0-9]+\.execute-api\." + re.escape(region) + r"\.amazonaws\.com", self.api)
                or self.login_url != f"https://aikea-cnc-{account}.auth.{region}.amazoncognito.com"
                or config["QuarantineBucket"] != self.quarantine_bucket
                or not re.fullmatch("[a-z0-9]{1,128}", client_id)):
            raise ValueError("Invalid AIkea gateway configuration.")
        if len(package) > 16_000_000:
            raise ValueError("Source ZIP exceeds the hosted intake's 16 MB limit.")
        self.http = http or CncHttpClient()
        self.login = login or CncBrowserLogin(self.login_url, client_id, self.http)
        self.access_token, self.uploaded = None, False

    def status(self):
        return {**super().status(), "sign_in_required": True}

    def _deliver(self, payload):
        # One network boundary translates known transport failures into retryable viewer errors.
        try:
            return self._send(payload)
        except HTTPError as error:
            if error.code == 400:
                body = error.read(65_536)
                try:
                    message = json.loads(body).get("error", "Request rejected.")
                except (ValueError, UnicodeDecodeError):
                    message = "Request rejected."
                raise QuoteDeliveryError(str(message)) from error
            raise QuoteDeliveryError("CNC intake rejected the request. Sign in with an invited, verified account and retry.") from error
        except (URLError, OSError) as error:
            raise QuoteDeliveryError("CNC upload connection failed. Retry this unchanged request.") from error

    def _send(self, payload):
        if not self.uploaded:
            files = {"source-repository.zip": self.package, "preview.png": payload.preview}
            request = {"request_id": self.request_id, "model_sha256": self.model_sha256, "preferences": payload.preferences,
                       "files": {name: {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()} for name, data in files.items()}}
            response = self._api("/requests", request)
            for name, data in files.items():
                self._upload(response["uploads"][name], name, data)
            self.uploaded = True
        return self._api(f"/requests/{self.request_id}/complete", {})

    def _api(self, path, body):
        if not self.access_token:
            self.access_token = self.login.authenticate()
        try:
            return self.http.json(self.api + path, body, self.access_token)
        except HTTPError as error:
            if error.code != 401:
                raise
        self.access_token = self.login.authenticate()
        return self.http.json(self.api + path, body, self.access_token)

    def _upload(self, grant, name, data):
        bucket = self.quarantine_bucket
        if grant["url"] not in {f"https://{bucket}.s3.amazonaws.com/", f"https://{bucket}.s3.{self.region}.amazonaws.com/"}:
            raise ValueError("Unexpected upload destination.")
        boundary = "aikea-" + secrets.token_hex(24)
        chunks = []
        for key, value in grant["fields"].items():
            if not re.fullmatch("[A-Za-z0-9_-]+", key):
                raise ValueError("Invalid upload field.")
            chunks.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{value}\r\n'.encode())
        chunks.append(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{name}"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode())
        chunks.extend([data, f"\r\n--{boundary}--\r\n".encode()])
        self.http.post(grant["url"], b"".join(chunks), {"Content-Type": "multipart/form-data; boundary=" + boundary})
