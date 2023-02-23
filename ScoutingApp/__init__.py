from . import competition
from flask import Flask, redirect, render_template, send_file, url_for; import flask.app
from flask_sqlalchemy import SQLAlchemy
import json
import os
import traceback
import waitress #production quality WSGI server to host the flask app with. more: https://docs.pylonsproject.org/projects/waitress/en/stable/index.html

STATIC = os.path.abspath("static")
TEMPLATES = os.path.abspath("templates")
#https://flask-sqlalchemy.palletsprojects.com/en/2.x/binds/
#https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application
DB_DIR = os.getcwd()
DB_BINDS = {}

app = Flask(__name__, static_folder=STATIC, template_folder=TEMPLATES)
app.url_map.strict_slashes = False
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(DB_DIR, '.db')}" #sadly, there needs to be an empty db, perhaps some day it will find its use
db = SQLAlchemy()

comps:"list[competition.Competition]" = []
not_content = []

def not_content_route(rule:str, onto=app, **options):
    "Mark route as a not-content-returning route. Internally uses route decorator with the object passed to onto. Default is app."
    def decor(f):
        not_content.append(rule)
        return onto.route(rule, **options)(f)
    return decor

#define routes
#for info on decorators, see https://realpython.com/primer-on-python-decorators/, or look up "python decorators"
@not_content_route("/")
def to_first_page():
    return redirect(url_for(compselect.__name__))

@app.route("/manifest.json")
def get_manifest():
    return send_file(os.path.abspath("manifest.json"))

@not_content_route("/sw.js")
def get_serviceworker():
    return send_file(os.path.join(STATIC, "js", "sw.js"))

@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/help.html")
def help():
    return render_template("help.html")

@app.route("/compselect.html")
def compselect():
    return render_template("compselect.html", competitions={comp.display_name:f"/comps/{comp.name}/{comp.start_url}" for comp in comps})

#api routes
#cite: https://stackoverflow.com/a/13318415
def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def _get_static_routes(dir=STATIC, name="static")->"list[str]":
    rtv = []
    for filename in os.listdir(dir):
        path = os.path.join(dir, filename)
        if os.path.isdir(path):
            rtv.extend(_get_static_routes(path, name=name+"/"+filename))
        elif os.path.isfile(path):
            rtv.append(f"/{name}/{filename}")
    return rtv

@not_content_route("/assets")
def assets():
    routes = list({
        url_for(rule.endpoint, **(rule.defaults or {}))
        for rule in app.url_map.iter_rules()
        if "GET" in rule.methods and has_no_empty_params(rule) and url_for(rule.endpoint, **(rule.defaults or {})) not in not_content
    })
    return json.dumps(routes+_get_static_routes())

@not_content_route("/ping")
def ping():
    return "pong" #TODO return something more useful later


#functions

def serve(host:str="localhost", port:int=8080):
    "Serve the webapp."
    print("Serving", host, f"on port {port}.")
    app.config["SQLALCHEMY_BINDS"] = DB_BINDS
    db.init_app(app)
    with app.app_context():
        db.create_all()
    waitress.serve(app, host=host, port=int(port), threads=48)

def load_competitions(dir:str=competition.COMPETITIONS_DIR):
    "Load competition blueprints from the competitions folder. Default is 'comps'."
    dir = os.path.abspath(dir)
    for filename in os.listdir(dir): #get paths to all files
        path = os.path.join(dir, filename)
        if os.path.isdir(path):
            path = os.path.join(path, "__init__.py")
        if os.path.isfile(path) and path.endswith((".py", ".pyw")):
            try:
                comp = competition.import_competition(path, filename)
            except:
                traceback.print_exc() #print caught exception's traceback and message, continue
            else:
                #handle the rest outside of try as to not skip over any exceptions raised here
                add_competition(comp)
                print(f"Loaded blueprint for competition '{comp.name}'.")

def add_competition(comp:competition.Competition):
    "Add the competition to the list if it hasn't already been added, register its blueprint."
    if comp in comps:
        return
    app.register_blueprint(comp.blueprint)
    comps.append(comp)
    if comp.db_uri is not None:
        DB_BINDS[comp.name] = comp.db_uri