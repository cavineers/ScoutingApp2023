from . import constants, data_manage, routes
from ScoutingApp import competition

__competition__ = competition.Competition("2023", "2023: Charged Up", "home.html", constants.DB_URI, routes.blueprint)