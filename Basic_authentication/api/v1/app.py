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
auth_type = getenv("AUTH_TYPE")
if auth_type == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()

@app.before_request
def before_request_func():
    """ Filter each request before processing """
    if auth is None:
        return

    # Autentifikasiya tələb olunmayan istisnalar siyahısı
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]

    # Əgər cari path istisnalar siyahısında yoxdursa, yoxlamalara başla
    if not auth.require_auth(request.path, excluded_paths):
        return

    # Authorization header yoxdursa, 401 Unauthorized qaytar
    if auth.authorization_header(request) is None:
        abort(401)

    # Cari istifadəçi tapılmırsa, 403 Forbidden qaytar
    if auth.current_user(request) is None:
        abort(403)


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
