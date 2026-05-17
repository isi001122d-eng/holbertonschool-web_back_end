#!/usr/bin/env python3
""" Module of Session Authentication views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """ POST /api/v1/auth_session/login
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Zəncirvari import xətasının qarşısını almaq üçün funksiya daxilində import edirik
    from api.v1.app import auth

    # Sessiya yaradırıq
    session_id = auth.create_session(user.id)

    # Cavab obyektini hazırlayırıq
    response = jsonify(user.to_json())

    # Kukini mühit dəyişənindəki adla response-a bağlayırıq
    cookie_name = getenv('SESSION_NAME')
    response.set_cookie(cookie_name, session_id)

    return response
