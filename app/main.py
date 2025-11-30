from flask import Blueprint, current_app, jsonify, request

from .auth import create_token, require_token

bp = Blueprint("main", __name__)

# Simple in-memory user store and balances for demo purposes
USERS = {
    "alice": {"password": "password1", "balance": 1000.0},
    "bob": {"password": "password2", "balance": 500.0},
}


@bp.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is running"})


@bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    user = USERS.get(username)
    if not user or user.get("password") != password:
        return jsonify({"error": "invalid credentials"}), 401

    token = create_token({"sub": username}, current_app.config.get("SECRET_KEY", "dev-secret"))
    return jsonify({"token": token})


@bp.route("/balance", methods=["GET"])
@require_token
def balance(user):
    u = USERS.get(user)
    if u is None:
        return jsonify({"error": "user not found"}), 404
    return jsonify({"user": user, "balance": u.get("balance", 0.0)})


@bp.route("/transfer", methods=["POST"])
@require_token
def transfer(user):
    data = request.get_json() or {}
    to_user = data.get("to")
    amount = float(data.get("amount", 0))

    if amount <= 0:
        return jsonify({"error": "invalid amount"}), 400

    from_account = USERS.get(user)
    to_account = USERS.get(to_user)
    if from_account is None or to_account is None:
        return jsonify({"error": "invalid account"}), 404

    if from_account["balance"] < amount:
        return jsonify({"error": "insufficient funds"}), 400

    from_account["balance"] -= amount
    to_account["balance"] += amount

    return jsonify({"status": "success", "from": user, "to": to_user, "amount": amount})
