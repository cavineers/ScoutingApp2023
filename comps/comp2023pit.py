from Scouting2023 import competition, STATIC, TEMPLATES
from flask import Blueprint, render_template
import os

blueprint = Blueprint("2023pit", __name__, url_prefix="/comps/2023pit", static_folder=STATIC, template_folder=TEMPLATES)

@blueprint.route("/pit.html")
def pit():
    return render_template("2023pit/pit.html")

__competition__ = competition.Competition("2023pit", "2023: Pit Scouting", "pit", blueprint)
