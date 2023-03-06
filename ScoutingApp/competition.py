from flask import Blueprint
import importlib.util
import inspect
import os
import sys

COMPETITIONS_DIR = os.path.abspath("comps")

class NoCompetitionException(Exception):
    "File does not specify a Competition object."

class Competition:
    "Object representing a competition."
    def __init__(self, name:str, display_name:str, start_url:str, blueprint:Blueprint):
        self.name = name
        self.display_name = display_name
        self.start_url = start_url
        self.blueprint = blueprint
        self.module = None

def import_competition(path:str, name:str=...)->Competition:
    "Imports the competition-specific code file."
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File {path} does not exist.")
    name = os.path.split(path)[1].rsplit(".",1)[0] if name is ... else str(name)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    #add module to sys so that it works right with import
    sys.modules[name] = module
    spec.loader.exec_module(module)
    
    #get competition object
    if not hasattr(module, "__competition__"):
        raise NoCompetitionException(f"File {path} missing Competition object. Set it under the variable '__competition__'.")
    comp:Competition = module.__competition__
    comp.module = module
    return comp


def define(instance:Competition):
    "Defines the Competition instance as the target Competition of the file or package.\nIf being used in a package, this must be called in the '__init__.py' file."
    frame = inspect.currentframe().f_back #gets the info for where the function was called
    frame.f_globals["__competition__"] = instance #creates variable __competition__ in that place's global scope
    return instance