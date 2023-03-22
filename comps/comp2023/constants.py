from datetime import datetime, tzinfo
import os

PARSE_VERSION = "1.0"
CONTENT_MATCH = "match"
CONTENT_PIT = "pit"
LOCAL_TIMEZONE:tzinfo = datetime.now().astimezone().tzinfo

DIR = os.path.dirname(__file__)
NAMES_FILE = os.path.join(DIR, "names.txt")
SUBMISSIONS_FILE = os.path.join(DIR, "submissions.txt") #each line is the json for one submission
SHEETS_TOKEN_FILE = os.path.join(DIR, "token.json")

#API names
API_KEYS_FILE = os.path.join(DIR, "apikeys.json")
SHEETS_OAUTH = "Sheets OAuth"
SHEETS_SCOPES = "https://www.googleapis.com/auth/spreadsheets",

SPREADSHEET_ID = "1KCPyhZ5O3CdlRzDyMer7pqnJjNJhin79JegNVN5Jo5M"

SHEETS_COLUMN_NAMES = {
    "TEAM NUMBER":"team_number",
    "MATCH NUMBER":"match_number",
    "DATE":"date",
    "SCOUTER":"scouter",
    "CONES SCORED BOTTOM":"cones_bottom",
    "CONES SCORED MIDDLE":"cones_middle",
    "CONES SCORED TOP":"cones_top",
    "CUBES SCORED BOTTOM":"cubes_bottom",
    "CUBES SCORED MIDDLE":"cubes_middle",
    "CUBES SCORED TOP":"cubes_top",
    "CONES TOTAL":"cones_total",
    "CUBES TOTAL":"cubes_total",
    "TOTAL PIECES":"total_pieces",
    "CONES AUTO":"cones_auto",
    "CUBES AUTO":"cubes_auto",
    "CONES TELEOP":"cones_teleop",
    "CUBES TELEOP":"cubes_teleop",
    "PICKED UP GROUND":"picked_up_ground",
    "PICKED UP SHELF":"picked_up_shelf",
    "DROPS":"drops",
    "CHARGING PAD STATE: AUTO":"charging_pad_auto",
    "CHARGING PAD STATE: TELEOP":"charging_pad_teleop",
    "DEFENSES":"defenses",
    "MIN SCORE DELTA":"min_score_delta",
    "MAX SCORE DELTA":"max_score_delta",
    "AVG SCORE DELTA":"avg_score_delta",
    "AUTO ACTIVITY":"auto_activity",
    "TELEOP ACTIVITY":"teleop_activity",
    "COMMENTS":"comments"
}

DATA_ATTR_NAMES = {v:k for k,v in SHEETS_COLUMN_NAMES.items()}

#various key and state names
class EventActions:
    PICK_UP = "pick_up"
    PICK_UP_SHELF = "shelf_pick_up"
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
    DATE = "date"
    PRELIMINARY_DATA = "preliminaryData"
    TEAM_NUMBER = "teamNumber"
    MATCH_NUMBER = "matchNumber"
    SCOUTER_NAME = "scouterName"
    SCORE = "scoreGrid"
    PICKUPS = "pickUps"
    SHELF_PICKUPS = "shelfPickUps"
    DROPS = "pieceDrops"
    DEFENSES = "defenses"
    CHARGE_STATE_AUTO = "autoChargeState"
    CHARGE_STATE = "chargeState"
    COMMENTS = "comments"
    NAV_STAMPS = "navStamps"
    END_AUTO = "endAuto"
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
class ScoreAwardName:
    MOBILITY = "MOBILITY"
    GAME_PIECES = "GAME PIECES"
    LINK = "LINK"
    PARK = "PARK"
    DOCKED = "DOCKED and not ENGAGED"
    ENGAGED = "DOCKED and ENGAGED"
    WIN = "Win"
    TIE = "Tie"
    #---Bonuses---
    SUSTAINABILITY = "SUSTAINABILITY BONUS"
    COOPERATION = "COOPERATION BONUS"
    ACTIVATION = "ACTIVATION BONUS"

class ScoreGridRow:
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"

SCORE_GRID_INDEX = (0, 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17), (1, 4, 7, 10, 13, 16), (18, 19, 20, 21, 22, 23, 24, 25, 26)
SCORE_GRID_NAMES = ScoreNodeType.CONE, ScoreNodeType.CUBE, ScoreNodeType.HYBRID

COOP_SCORE_NODES = (3, 4, 5, 12, 13, 14, 21, 22, 23) #middle 3 for each row

SCORE_GRID_ROW_INDEX = (0, 1, 2, 3, 4, 5, 6, 7, 8), (9, 10, 11, 12, 13, 14, 15, 16, 17), (18, 19, 20, 21, 22, 23, 24, 25, 26)
SCORE_GRID_ROW_NAMES = ScoreGridRow.TOP, ScoreGridRow.MIDDLE, ScoreGridRow.BOTTOM

#add 1 for auto
SCORE_VALUE_NAME = {
    ScoreGridRow.TOP: 5,
    ScoreGridRow.MIDDLE: 3,
    ScoreGridRow.BOTTOM: 2
}
SCORE_VALUE_INDEX = {
    SCORE_GRID_ROW_INDEX[0]: 5,
    SCORE_GRID_ROW_INDEX[1]: 3,
    SCORE_GRID_ROW_INDEX[2]: 2
}
