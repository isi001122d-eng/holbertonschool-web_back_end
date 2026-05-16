#!/usr/bin/env python3
""" Route module for the API """
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# auth dəyişənini ilkin olaraq None təyin edirik
auth = None

# AUTH_TYPE mühit dəyişəninə görə uyğun klası yükləyirik
# AUTH_TYPE mühit dəyişəninə görə uyğun klası yükləyirik
# AUTH_TYPE mühit dəyişəninə görə uyğun klası yükləyirik
auth_type = getenv("AUTH_TYPE")
if auth_type == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_type == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()

@app.before_request
def before_request_func():
    """ Filter each request before processing """
    if auth is None:
        return

    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]

    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None:
        abort(401)

    # current_user-i tapırıq
    user = auth.current_user(request)
    if user is None:
        abort(403)
    
    # Tapılan istifadəçini request obyektinə bağlayırıq (Tələb olunan hissə)
    request.current_user = user


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5100")
    app.run(host=host, port=port)
