from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt

auth_bp = Blueprint("auth_bp", __name__)

USERS = {"admin": bcrypt.hashpw(b"securepass", bcrypt.gensalt())}

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    username = data.get("username")
    password = (data.get("password") or "").encode()
    if username in USERS and bcrypt.checkpw(password, USERS[username]):
        return jsonify(access_token=create_access_token(identity=username))
    return jsonify({"msg": "Invalid credentials"}), 401
