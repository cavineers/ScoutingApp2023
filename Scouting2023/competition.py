from flask import Blueprint
import importlib.util
import os
import sys

COMPETITIONS_DIR = "comps"

class NoCompetitionException(Exception):
    "File does not specify a Competition object."

class Competition:
    def __init__(self, name:str, display_name:str, start_url:str, blueprint:Blueprint):
        self.name = name
        self.display_name = display_name
        self.start_url = start_url
        self.blueprint = blueprint
        self.module = None


def import_competition(path:str)->Competition:
    "Imports the competition-specific code file."
    if os.path.isdir(path):
        path = os.path.join(path, "__init__.py")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File {path} does not exist.")
    name = os.path.basename(path).rsplit(".",1)[0]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    #add module to sys so that it works right with import
    sys.modules[name] = module
    #get competition object
    module.__competition__
    if not hasattr(module, "__competition__"):
        raise NoCompetitionException(f"File {path} missing Competition object. Set it under the variable '__competition__'.")
    comp:Competition = module.__competition__
    comp.module = module
    return comp