import os
os.chdir(os.path.dirname(__file__))

from ScoutingApp import __main, app, load_competitions

load_competitions()

if __name__ == "__main__":
    __main.main(**{a[0]:a[1] for a in __main._get_args() if len(a)==2})