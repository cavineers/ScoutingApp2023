from . import constants, data_manage, routes
from ScoutingApp import competition

competition.define(competition.Competition("2023", "2023: Charged Up", "home.html", routes.blueprint))