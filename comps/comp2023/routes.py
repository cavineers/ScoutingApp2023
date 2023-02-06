from . import data_manage
from datetime import datetime
from ScoutingApp import db, not_content_route, STATIC, TEMPLATES
from flask import Blueprint, render_template, request
import traceback

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
@not_content_route("/upload", onto=blueprint, methods=["POST"])
def upload():
    try:
        if "data" in request.files:
            data = data_manage.load_qr_code(request.files[UPLOAD_DATA_KEY])
        elif UPLOAD_DATA_KEY in request.form:
            data = data_manage.load_json_data(request.form[UPLOAD_DATA_KEY])
        else:
            return f"You must upload a QR code or JSON data under key '{UPLOAD_DATA_KEY}'.", 400
    except Exception as e:
        traceback.print_exception(e)
        return "Got error while processing uploaded data.", 500
    
    try:
        data.submission_time = data_manage.to_utc_timestamp(datetime.now())
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        traceback.print_exception(e)
        return "Got error while committing uploaded data.", 500
    else:
        print(request.remote_addr, "uploaded data:", repr(data))
        return "Committed uploaded data.", 200