try : from .constants import *  #package import
except: from constants import * #module import (for DEBUG __main__ below)
from collections.abc import Mapping
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
import json
from PIL import Image
from pyzbar import pyzbar

class DataFields(Mapping):
    "Object for accessing data gotten from scouting a match."

    @classmethod
    def get(cls, data:dict):
        return cls(
            version=data.get(ContentKeys.VERSION),
            content_type=data.get(ContentKeys.CONTENT_TYPE),
            preliminary_data=data.get(ContentKeys.PRELIMINARY_DATA),
            score=data.get(ContentKeys.SCORE),
            pickups=data.get(ContentKeys.PICKUPS),
            drops=data.get(ContentKeys.DROPS),
            defenses=data.get(ContentKeys.DEFENSES),
            charge_state=data.get(ContentKeys.CHARGE_STATE),
            comments=data.get(ContentKeys.COMMENTS)
        )

    def __init__(self, version:str=None, content_type:str=None, preliminary_data:"dict[str]"=None, score:"dict[int, dict[int, str|None]]"=None,
                 pickups:"list[int]"=None, drops:"list[int]"=None, defenses:"list[int]"=None, charge_state:str=None, comments:"list[str]"=None):
        self.version = version
        self.content_type = content_type
        self.preliminary_data = preliminary_data
        self.score = score
        self.pickups = pickups
        self.drops = drops
        self.defenses = defenses
        self.charge_state = charge_state
        self.comments = comments

    def __getitem__(self, key:str): return self.__dict__[key]
    def __setitem__(self, key:str, value): self.__dict__[key] = value
    def __contains__(self, key:str): return key in self.__dict__
    def __len__(self):
        return len(tuple(iter(self)))
    def __iter__(self):
        for k in self.__dict__:
            if not k.startswith("__"):
                yield k

    @property
    def team_number(self)->int: return self.preliminary_data.get(ContentKeys.TEAM_NUMBER)
    @team_number.setter
    def team_number(self, value): self.preliminary_data[ContentKeys.TEAM_NUMBER] = value
    @property
    def match_number(self)->int: return self.preliminary_data.get(ContentKeys.MATCH_NUMBER)
    @match_number.setter
    def match_number(self, value): self.preliminary_data[ContentKeys.MATCH_NUMBER] = value
    @property
    def scouter_name(self)->str: return self.preliminary_data.get(ContentKeys.SCOUTER_NAME)
    @scouter_name.setter
    def scouter_name(self, value): self.preliminary_data[ContentKeys.SCOUTER_NAME] = value


    #construction methods
    def construct_score_events(self)->list:
        if ContentKeys.SCORE not in self:
            raise KeyError(ContentKeys.SCORE)
        events = []
        for index, history in self.score.items():
            for timestamp, game_piece in history.items():
                events.append(Event(
                    EventActions.SCORE,
                    from_utc_timestamp(timestamp),
                    self.team_number,
                    self.match_number,
                    self.scouter_name,
                    index=int(index)
                ))
        return events




#data base classes
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

class Match: #NOTE: this object should not be directly stored, should be constructed out 
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

    def all_events(self):
        "Get list of all events that happened during the match in chronoligical order."
        rtv = []
        for eventlist in self.events:
            rtv.extend(eventlist)
        rtv.sort(key=lambda e: e.time)
        return rtv

    def generate_grids(self, *team_numbers:int):
        "Return an object representing the score grid which contains the contributions of the given teams (by team number)."
        raise NotImplementedError("")

def from_utc_timestamp(value:int)->datetime:
    return datetime.fromtimestamp(value, tz=timezone.utc).astimezone(LOCAL_TIMEZONE)

def parse_qr_code(fp):
    "Parse the qr code and extract the JSON data"
    decoded:list = pyzbar.decode(Image.open(fp))
    return json.loads(decoded[0].data.decode("ascii"))

def load_qr_code(fp):
    "Parses qr code data and turns it into usable objects for comparions and such."
    fields = parse_qr_code(fp)
    if not isinstance(fields, dict):
        raise TypeError(f"Expected QR code to contain JSON object (dict), got {type(fields).__name__}.")
    return DataFields.get(fields)


if __name__ == "__main__": #DEBUG
    from pprint import pprint
    path = r"C:\Users\tickl\Downloads\download.png"
    print("="*10+"RAW DATA"+"="*10)
    pprint(parse_qr_code(path))
    data:DataFields = load_qr_code(path)
    print("\n"+"="*10+"EXTRACTED DATA"+"="*10)
    for attr, value in data.items():
        print(attr+":",value)
    for attr, value in DataFields.__dict__.items():
        if isinstance(value, property):
            print(attr+":", getattr(data, attr))