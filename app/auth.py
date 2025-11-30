import base64
import hashlib
import hmac
import json
import time
from functools import wraps

from flask import current_app, jsonify, request


def create_token(payload: dict, secret: str, ttl: int = 3600) -> str:
    data = payload.copy()
    data["exp"] = int(time.time()) + ttl
    raw = json.dumps(data, separators=(",", ":")).encode()
    sig = hmac.new(secret.encode(), raw, hashlib.sha256).digest()
    token = base64.urlsafe_b64encode(raw + b"." + sig).decode()
    return token


def verify_token(token: str, secret: str):
    try:
        decoded = base64.urlsafe_b64decode(token.encode())
        raw, sig = decoded.rsplit(b".", 1)
        expected = hmac.new(secret.encode(), raw, hashlib.sha256).digest()
        if not hmac.compare_digest(expected, sig):
            return None
        data = json.loads(raw.decode())
        if data.get("exp", 0) < int(time.time()):
            return None
        return data
    except Exception:
        return None


def require_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth.split(" ", 1)[1]
        else:
            token = auth

        secret = current_app.config.get("SECRET_KEY", "dev-secret")

        payload = verify_token(token, secret)
        if not payload:
            return jsonify({"error": "invalid or expired token"}), 401

        user = payload.get("sub")
        return f(user, *args, **kwargs)

    return wrapper
