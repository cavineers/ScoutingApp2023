from Scouting2023 import competition, STATIC, TEMPLATES
from flask import Blueprint, render_template
import os

blueprint = Blueprint("2023", __name__, url_prefix="/comps/2023", static_folder=STATIC, template_folder=TEMPLATES)

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





__competition__ = competition.Competition("2023", "2023: Charged Up", "home.html", blueprint)