# -*- coding: utf-8 -*-

from hashlib import md5
from io import BytesIO
import json
import os
import random

from flask import Flask, render_template, url_for, abort, g, redirect, make_response, send_from_directory, jsonify, request, Response
from pyPdf import PdfFileWriter, PdfFileReader
from werkzeug.exceptions import NotFound


app = Flask(__name__)

DEBUG = os.environ.get('FLASK_DEBUG', False)
SECRET_KEY = "\xef\x1e,X\xb3\xae#\x7f\xa5\xa6\xec]7\xc6@\x03\x8cj\x99{\x95\xec\x85g"
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PDF_SRC_DIR = os.path.join(PROJECT_ROOT, 'static', 'pdf-src')
PDF_NUM_PAGES = 17

app.config.from_object(__name__)


def jsonpify(*args, **kwargs):
    resp = jsonify(*args, **kwargs)
    if request.args.get('callback', False):
        resp.data = "%s(%s);" % (request.args['callback'], resp.data)
    return resp


@app.route("/")
def index():
    return jsonpify(status="404 Not found")


@app.route("/randomize-publication/")
def randomize_publication():
    queue_id = md5(os.urandom(24)).hexdigest()
    return jsonpify(status="ok", queue_id=queue_id, pick_up_url=url_for('pick_up_publication', queue_id=queue_id))


@app.route("/publications/<queue_id>")
def pick_up_publication(queue_id):
    return jsonpify(status="ready", pdf_url="%s%s" % (request.host_url[:-1], url_for('download_publication', queue_id=queue_id)))


@app.route("/publications/<queue_id>/download")
def download_publication(queue_id):
    pages = ["%02d" % page_num for page_num in range(2, app.config['PDF_NUM_PAGES']+1)]
    random.shuffle(pages)
    page_files = ["%s/%s.pdf" % (PDF_SRC_DIR, page) for page in ['01'] + pages]

    output = PdfFileWriter()
    for page_file in page_files:
        page_pdf = PdfFileReader(file(page_file, "rb"))
        output.addPage(page_pdf.getPage(0))

    outputStream = BytesIO()
    output.write(outputStream)
    outputStream.seek(0)

    return Response(outputStream, mimetype='application/pdf')


if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
