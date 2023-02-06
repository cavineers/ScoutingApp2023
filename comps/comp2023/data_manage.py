from .constants import *
from collections.abc import Mapping
from datetime import datetime, timezone
import json
from PIL import Image
from pyzbar import pyzbar
from ScoutingApp import db
import sqlalchemy, sqlalchemy.orm

#cite: https://stackoverflow.com/a/43587551
class JSON(sqlalchemy.types.TypeDecorator):
    "Represents JSON encoded content." #sqlite is so easy to set up, yet so restrictive :(  ...oh well :)
    impl = sqlalchemy.Text
    def process_bind_param(self, value, dialect:sqlalchemy.Dialect):
        return value if value is None else json.dumps(value)
    def process_result_value(self, value, dialect:sqlalchemy.Dialect):
        return json.loads(value) if value is not None else value 

class MatchData(db.Model):
    "Object for accessing data gotten from scouting a match via submission."

    __bind_key__ = "2023" #NOTE: bind key must be name attribute set in the Comptetition object
    __tablename__ = "match_data"

    #define columns, where the "C_" prefix indicates a column
    C_ID = db.Column("id", db.Integer, primary_key=True)
    C_VERSION = db.Column("version", db.String)
    C_TEAM_NUMBER = db.Column("team_number", db.Integer)
    C_MATCH_NUMBER = db.Column("match_number", db.Integer)
    C_SCOUTER_NAME = db.Column("scouter_name", db.String)
    C_SCORE_HISTORY = db.Column("score_history", JSON)
    C_PICKUPS = db.Column("pickups", JSON)
    C_DROPS = db.Column("drops", JSON)
    C_DEFENSES = db.Column("defenses", JSON)
    C_CHARGE_STATE = db.Column("charge_state", db.String(16))
    C_COMMENTS = db.Column("comments", JSON)


    @classmethod
    def get(cls, data:dict):
        preliminary_data = data.get(ContentKeys.PRELIMINARY_DATA)
        return cls(
            version=data.get(ContentKeys.VERSION),
            team_number=preliminary_data.get(ContentKeys.TEAM_NUMBER),
            match_number=preliminary_data.get(ContentKeys.MATCH_NUMBER),
            scouter_name=preliminary_data.get(ContentKeys.SCOUTER_NAME),
            score=data.get(ContentKeys.SCORE),
            pickups=data.get(ContentKeys.PICKUPS),
            drops=data.get(ContentKeys.DROPS),
            defenses=data.get(ContentKeys.DEFENSES),
            charge_state=data.get(ContentKeys.CHARGE_STATE),
            comments=data.get(ContentKeys.COMMENTS)
        )

    def __init__(self, version:str=None, team_number:int=None, match_number:int=None, scouter_name:str=None, score:"dict[str, dict[str, str|None]]"=None,
                 pickups:"list[int]"=None, drops:"list[int]"=None, defenses:"list[int]"=None, charge_state:str=None, comments:"list[str]"=None):
        self.version = version
        self.team_number = team_number
        self.match_number = match_number
        self.scouter_name = scouter_name
        self.score = score
        self.pickups = pickups
        self.drops = drops
        self.defenses = defenses
        self.charge_state = charge_state
        self.comments = comments

    def __getitem__(self, key:str): return self.__dict__[key]
    def __setitem__(self, key:str, value): self.__dict__[key] = value
    def __contains__(self, key:str): return key in self.__dict__

    def __repr__(self):
        return f"<MatchData {self.id} from '{self.scouter_name}' at {hex(id(self))}>"

    @property
    def id(self)->int:
        if not (isinstance(self.team_number, int) and isinstance(self.match_number, int)):
            raise TypeError("MatchData team number and match number must both be of type int to generate a MatchData id.")
        #":04" will ensure that match number takes up at least 4 digits of space in the id, any untaken space is replaced with leading 0s
        return int(f"{self.team_number}{self.match_number:04}")

    @sqlalchemy.orm.reconstructor
    def _sql_reconstruct(self):
        "Runs after object is reconstructed from the database."
        self.__class__.__init__(
            self,
            version=self.C_VERSION,
            team_number=self.C_TEAM_NUMBER,
            match_number=self.C_MATCH_NUMBER,
            scouter_name=self.C_SCOUTER_NAME,
            score=self.C_SCORE_HISTORY,
            pickups=self.C_PICKUPS,
            drops=self.C_DROPS,
            defenses=self.C_DEFENSES,
            charge_state=self.C_CHARGE_STATE,
            comments=self.C_COMMENTS
        )

    #construction methods
    def construct_score_events(self)->"list[Event]":
        if self.score is None:
            raise KeyError(ContentKeys.SCORE)
        events = []
        for index, history in self.score.items():
            for timestamp, game_piece in history.items():
                #TODO link the PICKUP event that goes with this SCORE event later
                events.append(Event(
                    EventActions.SCORE,
                    from_utc_timestamp(timestamp),
                    self.team_number,
                    self.match_number,
                    self.scouter_name,
                    index=int(index)
                ))
        return events

    def construct_drop_events(self)->"list[Event]":
        if self.drops is None:
            raise KeyError(ContentKeys.DROPS)
        #TODO link the PICKUP event that goes with this DROP event later
        return [Event(EventActions.DROP, from_utc_timestamp(timestamp), self.team_number, self.match_number, self.scouter_name) for timestamp in self.drops]

    def contruct_defense_events(self)->"list[Event]":
        if self.defenses is None:
            raise KeyError(ContentKeys.DEFENSES)
        return [Event(EventActions.DEFENSE, from_utc_timestamp(timestamp), self.team_number, self.match_number, self.scouter_name) for timestamp in self.defenses]

    def construct_pickup_events(self)->"list[Event]":
        if self.pickups is None:
            raise KeyError(ContentKeys.PICKUPS)
        return [Event(EventActions.PICK_UP, from_utc_timestamp(timestamp), self.team_number, self.match_number, self.scouter_name) for timestamp in self.pickups]


class Event:
    "Object representing an event that happened during the match."
    def __init__(self, action:str, time:datetime, team_number:int, match_number:int, scouter_name:str, **other):
        self.action = action
        self.time = time
        #reference fields: can be used in database subclass to access the related objects
        self.team_number = team_number
        self.match_number = match_number
        self.scouter_name = scouter_name
        self._other = other
    
    def __getitem__(self, key:str): return self._other[key]
    def __setitem__(self, key:str, value): self._other[key] = value

    def __repr__(self):
        return f"<Event '{self.action}' : {self.time or '-'} at {hex(id(self))}>"

    def __gt__(self, value):
        if isinstance(value, Event):
            return self.time > value.time
        else:
            return super().__gt__(value)

    def __lt__(self, value):
        if isinstance(value, Event):
            return self.time < value.time
        else:
            return super().__lt__(value)

    def __eq__(self, value):
        if isinstance(value, Event):
            return self.time == value.time and self.action == value.action
        else:
            return super().__eq__(value)


class Match:
    "Collection of data for one match."

    def __init__(self, number:int, events:"dict[int, list[Event]]", scouters:"dict[str, int]"):
        self.number:int = number
        self.events = events #{team_number:[Event, ...], ...}
        self.scouters = scouters #{scouter_name:team_number, ...}

    def __repr__(self):
        return f"<Match #{self.number} at {hex(id(self))}>"

    def get_scouter_events(self, name:str):
        "Get events a team preformed during a match by name of scouter scouting the team."
        return self.events[self.scouters]

    def get_teams(self):
        "Get a set of all teams in this match."
        return set((*self.events, *self.scouters.values()))

    def all_events(self, *teams:int):
        "Get list of all events that happened during the match in chronoligical order."
        rtv = []
        for eventlist in self.events:
            rtv.extend(eventlist)
        rtv.sort(key=lambda e: e.time)
        return rtv

    def generate_grids(self, *team_numbers:int):
        "Return an object representing the score grid which contains the contributions of the given teams (by team number)."
        raise NotImplementedError

#functions
def from_utc_timestamp(value:int)->datetime:
    return datetime.fromtimestamp(value, tz=timezone.utc).astimezone(LOCAL_TIMEZONE)

def to_utc_timestamp(dt:datetime)->int:
    return int(dt.astimezone(timezone.utc).timestamp()*1000) #from seconds.microseconds -> milliseconds

def parse_qr_code(fp)->"dict[str]":
    "Parse the qr code and extract the JSON data"
    decoded:list = pyzbar.decode(Image.open(fp))
    return json.loads(decoded[0].data.decode("ascii"))

def load_qr_code(fp):
    "Parses qr code data and turns it into usable objects."
    return read_data(parse_qr_code(fp))
    
def load_json_data(data:str):
    "Parses JSON string and turns it into usable objects."
    return read_data(json.loads(data))

def read_data(fields:dict):
    "Read the given data (dict) and return the appropriate object."
    if not isinstance(fields, dict):
        raise TypeError(f"Expected dict, got {type(fields).__name__}.")
    elif ContentKeys.CONTENT_TYPE not in fields:
        raise KeyError(repr(ContentKeys.CONTENT_TYPE))

    content_type = str(fields.get(ContentKeys.CONTENT_TYPE)).strip().lower()
    if content_type == CONTENT_MATCH:
        return MatchData.get(fields)
    else:
        raise ValueError(f"Unknow content type '{content_type}'.")


def _debug(path:str): #debug used in scouting app presentation on 2/4/2023
    from pprint import pprint
    print("="*10+"RAW DATA"+"="*10)
    pprint(parse_qr_code(path))
    data:MatchData = load_qr_code(path)
    print("\n"+"="*10+"EXTRACTED DATA"+"="*10)
    for attr, value in data.items():
        print(attr+":",value)
    for attr, value in MatchData.__dict__.items():
        if isinstance(value, property):
            print(attr+":", getattr(data, attr))