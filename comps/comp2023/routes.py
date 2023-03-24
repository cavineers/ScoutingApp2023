from . import data_manage
from .constants import NAMES_FILE
from ScoutingApp import not_content_route, STATIC, TEMPLATES
from flask import Blueprint, render_template, request
import json
import traceback

blueprint = Blueprint("2023", __name__, url_prefix="/comps/2023", static_folder=STATIC, template_folder=TEMPLATES)


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

#api routes
UPLOAD_DATA_KEY = "data"
@not_content_route("/upload", onto=blueprint, methods=["POST"])
def upload():
    try:
        if UPLOAD_DATA_KEY in request.files:
            #data = data_manage.parse_qr_code(request.files[UPLOAD_DATA_KEY])
            return "Not accepting QR Codes anymore.", 400
        elif UPLOAD_DATA_KEY in request.form:
            data = json.loads(json.loads(request.form[UPLOAD_DATA_KEY]))
        else:
            return f"You must upload a QR code or JSON data under key '{UPLOAD_DATA_KEY}'.", 400
    except Exception as e:
        traceback.print_exception(e)
        return "Got error while reading uploaded data.", 500
    try:
        data_manage.handle_upload(data)
    except Exception as e:
        traceback.print_exception(e)
        return "Got error while storing uploaded data.", 500
    else:
        print(request.remote_addr, "uploaded data:", repr(data))
        return "Committed uploaded data.", 200
    
# @not_content_route("/submissions.txt", onto=blueprint)
# def get_submissions():
#     return send_file(SUBMISSIONS_FILE, "text")
    