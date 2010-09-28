# -*- coding: utf-8 -*-

import os.path

from flask import Flask, render_template, url_for, abort, g

DEBUG = os.environ.get('FLASK_DEBUG', False)

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/")
def index():
    return "Hello world!"


if __name__ == "__main__":
    app.run()
