from datetime import datetime, tzinfo
import os
from ScoutingApp import DB_DIR

PARSE_VERSION = "1.0"
CONTENT_MATCH = "match"
CONTENT_PIT = "pit"
LOCAL_TIMEZONE:tzinfo = datetime.now().astimezone().tzinfo
DB_URI = f"sqlite:///{os.path.join(DB_DIR, 'comp2023.db')}"
BIND_KEY = "2023" #NOTE: bind key must be name attribute set in the Comptetition object

class TableNames:
    MatchData = "match_data"
    Event = "events"
    Match = "matches"
    Scouter = "scouters"
class EventActions:
    PICK_UP = "pick_up"
    DROP = "drop"
    SCORE = "score"
    DEFENSE = "defense"
class ChargeStates:
    OFF = "off"
    DOCKED = "docked"
    ENGAGED = "engaged"
class ContentKeys:
    VERSION = "version"
    CONTENT_TYPE = "contentType"
    PRELIMINARY_DATA = "preliminaryData"
    TEAM_NUMBER = "teamNumber"
    MATCH_NUMBER = "matchNumber"
    SCOUTER_NAME = "scouterName"
    SCORE = "scoreGrid"
    PICKUPS = "pickUps"
    DROPS = "pieceDrops"
    DEFENSES = "defenses"
    CHARGE_STATE = "chargeState"
    COMMENTS = "comments"
    NAV_STAMPS = "navStamps"
class GamePiece:
    CONE = "cone"
    CUBE = "cube"
class ScoreNodeType:
    CONE = "cone"
    CUBE = "cube"
    HYBRID = "hybrid"
class ScoreType:
    TELEOP = "teleop"
    AUTO = "auto"
    RANKING = "ranking"
class ScoreGridRow:
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"

SCORE_GRID_INDEX = (0, 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17), (1, 4, 7, 10, 13, 16), (18, 19, 20, 21, 22, 23, 24, 25, 26)
SCORE_GRID_NAMES = ScoreNodeType.CONE, ScoreNodeType.CUBE, ScoreNodeType.HYBRID

COOP_SCORE_NODES = (3, 4, 5, 12, 13, 14, 21, 22, 23) #middle 3 for each row

SCORE_GRID_ROW_INDEX = (0, 1, 2, 3, 4, 5, 6, 7, 8), (9, 10, 11, 12, 13, 14, 15, 16, 17), (18, 19, 20, 21, 22, 23, 24, 25, 26)
SCORE_GRID_ROW_NAMES = ScoreGridRow.TOP, ScoreGridRow.MIDDLE, ScoreGridRow.BOTTOM
