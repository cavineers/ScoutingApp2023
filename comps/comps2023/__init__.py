from . import data_manage, routes
import Scouting2023.competition

__competition__ = Scouting2023.competition.Competition("2023", "2023: Charged Up", "home.html", routes.blueprint)