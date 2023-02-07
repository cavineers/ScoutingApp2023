from . import competition, db, serve, load_competitions
import sys

def main(**kw):
    load_competitions(kw.pop("dir", competition.COMPETITIONS_DIR))
    try:
        serve(**kw)
    finally:
        db.close()


def _get_args():
    for a in sys.argv[1:]:
        yield a.split("=",1)

if __name__ == "__main__":
    main(**{a[0]:a[1] for a in _get_args() if len(a)==2})