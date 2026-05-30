#!/usr/bin/env python3
"""Task 5: Mock logging in"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from typing import Optional, Dict


class Config:
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)

# Users table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


# Custom Babel class to override get_locale
class MyBabel(Babel):
    def get_locale(self):
        # Check if user has a preferred locale
        user = getattr(g, "user", None)
        if user:
            user_locale = user.get("locale")
            if user_locale in app.config["LANGUAGES"]:
                return user_locale

        # Fallback to URL param
        locale = request.args.get("locale")
        if locale in app.config["LANGUAGES"]:
            return locale

        # Fallback to request header
        return request.accept_languages.best_match(app.config["LANGUAGES"])


babel = MyBabel(app)


# Get user based on ?login_as=ID
def get_user() -> Optional[Dict]:
    try:
        user_id = int(request.args.get("login_as"))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """Executed before each request."""
    g.user = get_user()


@app.route("/")
def index():
    return render_template("5-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
