from . import data_manage
from Scouting2023 import STATIC, TEMPLATES
from flask import Blueprint, render_template, request
import json

blueprint = Blueprint("2023", __name__, url_prefix="/comps/2023", static_folder=STATIC, template_folder=TEMPLATES)

#content routes
@blueprint.route("/home.html")
def home():
    return render_template("2023/home.html")

@blueprint.route("/scout.html")
def scout():
    return render_template("2023/scout.html")

@blueprint.route("/auto.html")
def auto():
    return render_template("2023/auto.html")

@blueprint.route("/qrscanner.html")
def qr_scanner():
    return render_template("2023/qrscanner.html")

@blueprint.route("/result.html")
def result():
    return render_template("2023/result.html")


#api routes
UPLOAD_DATA_KEY = "data"
@blueprint.route("/upload", methods=["POST"])
def upload():
    if "data" in request.files:
        data = data_manage.parse_qr_code(request.files[UPLOAD_DATA_KEY])
    elif UPLOAD_DATA_KEY in request.form:
        data = json.loads(request.form[UPLOAD_DATA_KEY])
    else:
        return f"You must upload a QR code or JSON data under key '{UPLOAD_DATA_KEY}'.", 400