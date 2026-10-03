"""Scope: Route JWT-authorized intake calls without logging tokens or uploaded content."""

import base64
import json
import os

from botocore.exceptions import BotoCoreError, ClientError

from intake_acceptance import IntakeAcceptance
from intake_reservations import IntakeReservations
from intake_storage import IntakeStorage


class IntakeGateway:
    def __init__(self, storage, directory, pool):
        self.reservations = IntakeReservations(storage)
        self.acceptance = IntakeAcceptance(storage)
        self.directory, self.pool = directory, pool

    def handle(self, event):
        claims = event.get("requestContext", {}).get("authorizer", {}).get("jwt", {}).get("claims", {})
        if claims.get("token_use") != "access" or not claims.get("sub") or not claims.get("username"):
            return self.response(401, {"error": "Sign in to submit a request."})
        owner = self.reservations.owner(claims["sub"])
        # This is the sole HTTP error boundary; inner operations preserve AWS failures.
        try:
            raw = event.get("body", "")
            raw = base64.b64decode(raw, validate=True) if event.get("isBase64Encoded") else raw.encode()
            if len(raw) > 16_384:
                return self.response(413, {"error": "Request metadata exceeds limit."})
            body = json.loads(raw)
            route = event.get("routeKey")
            email = self._email(claims["username"])
            if route == "POST /requests":
                result = self.reservations.reserve(owner, body, email)
            elif route == "POST /requests/{request_id}/complete" and body == {}:
                result = self.acceptance.complete(owner, event["pathParameters"]["request_id"])
            else:
                return self.response(404, {"error": "Unknown intake route."})
            return self.response(200, result)
        except PermissionError as error:
            return self.response(403, {"error": str(error)})
        except (ValueError, UnicodeDecodeError) as error:
            return self.response(400, {"error": str(error)})
        except (BotoCoreError, ClientError):
            return self.response(503, {"error": "Upload service unavailable. Retry the same request."})

    def _email(self, username):
        user = self.directory.admin_get_user(UserPoolId=self.pool, Username=username)
        attributes = {item["Name"]: item["Value"] for item in user["UserAttributes"]}
        if not user["Enabled"] or attributes.get("email_verified") != "true":
            raise PermissionError("A verified email is required.")
        return attributes["email"]

    def response(self, status, body):
        return {"statusCode": status, "headers": {"Content-Type": "application/json", "Cache-Control": "no-store"},
                "body": json.dumps(body)}


# AWS requires a module-level handler; the gateway owns all request behavior.
def handler(event, context):
    import boto3
    from botocore.config import Config

    storage = IntakeStorage(boto3.client("s3", config=Config(signature_version="s3v4")),
                            os.environ["QUARANTINE_BUCKET"], os.environ["ACCEPTED_BUCKET"])
    return IntakeGateway(storage, boto3.client("cognito-idp"), os.environ["USER_POOL"]).handle(event)
