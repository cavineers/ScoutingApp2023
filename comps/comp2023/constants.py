from datetime import datetime, tzinfo
import os

PARSE_VERSION = "1.0"
CONTENT_MATCH = "match"
CONTENT_PIT = "pit"
LOCAL_TIMEZONE:tzinfo = datetime.now().astimezone().tzinfo

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
    END_AUTO = "end_auto"
    START = "start"
    END = "end"
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
