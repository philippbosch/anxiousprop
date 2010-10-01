# -*- coding: utf-8 -*-

import beanstalkc
from hashlib import md5
import json
import os
import random

from flask import Flask, render_template, url_for, abort, g, redirect, make_response, send_from_directory
from werkzeug.exceptions import NotFound

app = Flask(__name__)

DEBUG = os.environ.get('FLASK_DEBUG', False)
SECRET_KEY = "\xef\x1e,X\xb3\xae#\x7f\xa5\xa6\xec]7\xc6@\x03\x8cj\x99{\x95\xec\x85g"
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PDF_DIRECTORY = os.path.join(PROJECT_ROOT, app.static_path[1:], 'pdf')
PDF_NUM_PAGES = 28

app.config.from_object(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/randomize-publication/")
def randomize_publication():
    queue_id = md5(os.urandom(24)).hexdigest()
    beanstalk = beanstalkc.Connection()
    pages = ["%02d" % page_num for page_num in range(2, app.config['PDF_NUM_PAGES']+1)]
    random.shuffle(pages)
    beanstalk.put(json.dumps({'queue_id': queue_id, 'pages': pages}))
    return redirect(url_for('pick_up_publication', queue_id=queue_id))

@app.route("/publications/<queue_id>")
def pick_up_publication(queue_id):
    if os.path.exists(os.path.join(app.config['PDF_DIRECTORY'], '%s.pdf' % queue_id)):
        return render_template("pick-up-ready.html", queue_id=queue_id)
    else:
        response = make_response(render_template("pick-up-waiting.html", queue_id=queue_id))
        response.headers['Refresh'] = 3
        return response

@app.route("/publications/<queue_id>/download")
def download_publication(queue_id):
    try:
        return send_from_directory(app.config['PDF_DIRECTORY'], '%s.pdf' % queue_id, as_attachment=False, attachment_filename="The Anxious Prop - Case 3.pdf")
    except NotFound:
        return redirect(url_for('pick_up_publication', queue_id=queue_id))

if __name__ == "__main__":
    app.run('0.0.0.0')
