from . import competition
from flask import Flask, render_template, send_file
import os
import traceback
import waitress #production quality WSGI server to host the flask app with. more: https://docs.pylonsproject.org/projects/waitress/en/stable/index.html

STATIC = os.path.abspath("static")
TEMPLATES = os.path.abspath("templates")

app = Flask(__name__, static_folder=STATIC, template_folder=TEMPLATES)
app.url_map.strict_slashes = False

comps = []

#define routes
#for info on decorators, see https://realpython.com/primer-on-python-decorators/, or look up "python decorators"
@app.route("/manifest.json")
def get_manifest():
    return send_file(os.path.abspath("manifest.json"))

@app.route("/")
@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/help.html")
def help():
    return render_template("help.html")

@app.route("/compselect.html")
def compselect():
    return render_template("compselect.html")


#functions
def serve(host:str="localhost", port:int=8080):
    "Serve the webapp."
    print("Serving", host, f"on port {port}.")
    waitress.serve(app, host=host, port=int(port), threads=48)

def load_competitions(dir:str=competition.COMPETITIONS_DIR):
    "Load competition blueprints from the competitions folder. Default is 'comps'."
    for filename in os.listdir(dir): #get paths to all files 
        path = os.path.join(dir, filename)
        #skip file if it does not end with .py or .pyw, or skip folder if it does not contain file __init__.py or __init__.pyw
        if not (os.path.isfile(path) or path.endswith((".py", ".pyw"))) and all(not os.path.isdir(os.path.join(path, fn)) for fn in ("__init__.py", "__init__.pyw")):
            continue
        try:
            comp = competition.import_competition(path)
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