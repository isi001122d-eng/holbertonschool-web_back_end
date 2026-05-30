#!/usr/bin/env python3
from flask import Flask, render_template, request
from flask_babel import Babel, _


class Config(object):
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)


# Sous-classe pour gérer la locale dynamique
class MyBabel(Babel):
    def get_locale(self):
        locale = request.args.get("locale")
        if locale in app.config["LANGUAGES"]:
            return locale
        return super().get_locale()


babel = MyBabel(app)


@app.route("/")
def index():
    return render_template("4-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
