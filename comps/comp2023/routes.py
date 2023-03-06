from . import data_manage
from datetime import datetime
from ScoutingApp import not_content_route, STATIC, TEMPLATES
from flask import Blueprint, render_template, request
import json
import os
import traceback

blueprint = Blueprint("2023", __name__, url_prefix="/comps/2023", static_folder=STATIC, template_folder=TEMPLATES)

NAMES_FILE = os.path.join(os.path.dirname(__file__), "names.txt")

#content routes
@blueprint.route("/home.html")
def home():
    with open(NAMES_FILE) as f:
        return render_template("2023/home.html", names=sorted([name.strip() for name in f.readlines()], key=lambda name: name.rsplit(" ",1)[-1]))

@blueprint.route("/scout.html")
def scout():
    return render_template("2023/scout.html")

@blueprint.route("/prematch.html")
def auto():
    return render_template("2023/prematch.html")

@blueprint.route("/qrscanner.html")
def qr_scanner():
    return render_template("2023/qrscanner.html")

@blueprint.route("/result.html")
def result():
    return render_template("2023/result.html")

@blueprint.route("/names")
def names():
    with open(NAMES_FILE) as f:
        return json.dumps([name.strip() for name in f.readlines()])

@blueprint.route("/sheets")
def sheets():
    return ""


#api routes
UPLOAD_DATA_KEY = "data"
@not_content_route("/upload", onto=blueprint, methods=["POST"])
def upload():
    try:
        if "data" in request.files:
            data = data_manage.parse_qr_code(request.files[UPLOAD_DATA_KEY])
        elif UPLOAD_DATA_KEY in request.form:
            data = json.loads(request.form[UPLOAD_DATA_KEY])
        else:
            return f"You must upload a QR code or JSON data under key '{UPLOAD_DATA_KEY}'.", 400
    except Exception as e:
        traceback.print_exception(e)
        return "Got error while reading uploaded data.", 500
    
    #TODO process data into column values (see: https://docs.google.com/spreadsheets/d/1KCPyhZ5O3CdlRzDyMer7pqnJjNJhin79JegNVN5Jo5M/edit#gid=0 )
    
    try:
        ... #TODO add data to sheets
    except Exception as e:
        traceback.print_exception(e)
        return "Got error while storing uploaded data.", 500
    else:
        print(request.remote_addr, "uploaded data:", repr(data))
        return "Committed uploaded data.", 200