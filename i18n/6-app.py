#!/usr/bin/env python3
"""Task 6: Use user locale with Flask and Babel"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from typing import Dict, Optional


class Config:
    """
    Configuration class for Flask app
    Defines available languages, default locale and timezone
    """

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)

# Simulated user database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class MyBabel(Babel):
    """
    Custom Babel class to override get_locale method and set
    locale preference based on priority:
    1. Locale from URL parameter (?locale=fr)
    2. Locale from logged-in user settings
    3. Locale from request headers (browser)
    """

    def get_locale(self):
        """
        Determine best matching locale to use for the request
        """
        # Priority 1: URL argument
        locale = request.args.get("locale")
        if locale and locale in app.config["LANGUAGES"]:
            return locale

        # Priority 2: User locale if available
        user = getattr(g, "user", None)
        if user:
            user_locale = user.get("locale")
            if user_locale in app.config["LANGUAGES"]:
                return user_locale

        # Priority 3: Accept-Language header
        return request.accept_languages.best_match(app.config["LANGUAGES"])


# Initialize custom Babel
babel = MyBabel(app)


def get_user() -> Optional[Dict]:
    """
    Retrieves user dictionary from the simulated users database
    using login_as URL parameter (e.g. ?login_as=2)

    Returns:
        dict or None: User dict if valid user ID provided, otherwise None
    """
    try:
        user_id = int(request.args.get("login_as"))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """
    Set user globally before handling the request.
    This allows the user to be accessed anywhere in the request lifecycle.
    """
    g.user = get_user()


@app.route("/")
def index():
    """
    Render the main index page using the appropriate locale
    """
    return render_template("6-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
