#!/usr/bin/env python3
"""
2-app.py - A Flask application with locale detection using babel.init_app().
"""

from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """Configuration class for Flask app."""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)


def get_locale():
    """Select the best language match from the user's request."""
    return request.accept_languages.best_match(app.config["LANGUAGES"])


babel = Babel()
babel.init_app(app, locale_selector=get_locale)


@app.route("/")
def index():
    """Render the index page."""
    return render_template("2-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
