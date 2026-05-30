#!/usr/bin/env python3
"""
Flask app with i18n and timezone support
"""
from flask import Flask, request, render_template, g
from flask_babel import Babel, _
import pytz
from pytz.exceptions import UnknownTimeZoneError

app = Flask(__name__)


class Config(object):
    """
    App configuration for Babel
    """

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)

# Simulated user database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_locale():
    """
    Determine the best language for the user
    Priority: URL parameter > User settings > Request headers > Default
    """
    locale = request.args.get("locale")
    if locale in app.config["LANGUAGES"]:
        return locale

    user = getattr(g, "user", None)
    if user:
        user_locale = user.get("locale")
        if user_locale in app.config["LANGUAGES"]:
            return user_locale

    return request.accept_languages.best_match(app.config["LANGUAGES"])


def get_timezone():
    """
    Determine the appropriate time zone
    Priority: URL parameter > User settings > Default (UTC)
    """
    tz_param = request.args.get("timezone")
    if tz_param and tz_param in pytz.all_timezones:
        return tz_param

    user = getattr(g, "user", None)
    if user:
        user_tz = user.get("timezone")
        if user_tz and user_tz in pytz.all_timezones:
            return user_tz

    return app.config["BABEL_DEFAULT_TIMEZONE"]


# Initialize Babel
babel = Babel(app, locale_selector=get_locale, timezone_selector=get_timezone)


def get_user():
    """
    Retrieve user dict from login_as URL param
    """
    try:
        user_id = int(request.args.get("login_as"))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """
    Set the current user in the global object g
    """
    g.user = get_user()


@app.route("/")
def hello_world():
    """
    Render the homepage template
    """
    return render_template("6-index.html")
