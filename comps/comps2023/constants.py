from datetime import datetime, tzinfo
import os
from ScoutingApp import DB_PATH as DB_DIR

PARSE_VERSION = "1.0"
CONTENT_MATCH = "match"
CONTENT_PIT = "pit"
LOCAL_TIMEZONE:tzinfo = datetime.now().astimezone().tzinfo
DB_URI = f"sqlite:///{os.path.join(DB_DIR, 'comp2023.db')}"


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
class GamePiece:
    CONE = "cone"
    CUBE = "cube"