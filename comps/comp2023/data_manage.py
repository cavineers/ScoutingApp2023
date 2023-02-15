from .constants import *
from datetime import datetime, timedelta, timezone
import json
from PIL import Image
from pyzbar import pyzbar
from ScoutingApp import db
import sqlalchemy, sqlalchemy.orm


#NOTE: the notes below are about scoring, points, etc
#cite: see manual 6.4:44-45 for time period between action taking place and when it counts for points 
#cite: see manual 6.4.1:45 for scoring criteria
#cite: see manual 6.4.3:46-47 for point values

#cite: https://stackoverflow.com/a/43587551
class Json(sqlalchemy.TypeDecorator):
    "Represents JSON encoded content." #sqlite is so easy to set up, yet so restrictive :(  ...oh well :)
    impl = sqlalchemy.Text
    def process_bind_param(self, value, dialect):
        return value if value is None else json.dumps(value)
    def process_result_value(self, value, dialect):
        return json.loads(value) if value is not None else value
    
class Datetime(sqlalchemy.TypeDecorator):
    "Represents datetime object."
    impl = sqlalchemy.Integer
    def process_bind_param(self, value:datetime, dialect):
        return to_utc_timestamp(value) if isinstance(value, datetime) else None
    def process_result_value(self, value:int, dialect):
        return from_utc_timestamp(value) if isinstance(value, int) else None


class MatchData(db.Model):
    "Object for accessing data gotten from scouting a match via submission."

    __bind_key__ = BIND_KEY
    __tablename__ = TableNames.MatchData

    #define columns
    id = db.Column("id", db.Integer, primary_key=True)
    version = db.Column("version", db.String, nullable=True)
    team_number = db.Column("team_number", db.Integer, nullable=True)
    match_number = db.Column("match_number", db.Integer, nullable=True)
    scouter_name = db.Column("scouter_name", db.String, nullable=True)
    score = db.Column("score_history", Json, nullable=True)
    pickups = db.Column("pickups", Json, nullable=True)
    drops = db.Column("drops", Json, nullable=True)
    defenses = db.Column("defenses", Json, nullable=True)
    charge_state = db.Column("charge_state", db.String(16), nullable=True)
    comments = db.Column("comments", Json, nullable=True)
    submission_time = db.Column("submission_time", db.Integer, nullable=True)
    #navigational timestamps
    navigation_start = db.Column("navigation_start", db.Integer, nullable=True) #to home.html
    navigation_prematch = db.Column("navigation_prematch", db.Integer, nullable=True) #to prematch.html
    navigation_match = db.Column("navigation_match", db.Integer, nullable=True) #to scout.html
    navigation_result = db.Column("navigation_result", db.Integer, nullable=True) #to result.html
    navigation_finish = db.Column("navigation_finish", db.Integer, nullable=True) #to qrscanner.html


    @staticmethod
    def get(id:int)->"MatchData|None":
        "Query for the MatchData object by ID."
        return filter_search(MatchData, id=id).first()

    @staticmethod
    def search(**by):
        "Query for the MatchData object by the given criteria."
        return filter_search(MatchData, by)


    @classmethod
    def generate(cls, data:dict):
        "Create a MatchData object from raw data."
        preliminary_data = data.get(ContentKeys.PRELIMINARY_DATA,{})
        nav_stamps = data.get(ContentKeys.NAV_STAMPS,{})
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
            comments=data.get(ContentKeys.COMMENTS),
            navigation_start=nav_stamps.get("home.html"),
            navigation_prematch=nav_stamps.get("prematch.html"),
            navigation_match=nav_stamps.get("scout.html"),
            navigation_result=nav_stamps.get("result.html"),
            navigation_finish=nav_stamps.get("qrscanner.html")
        )

    def __init__(self, version:str=None, team_number:int=None, match_number:int=None, scouter_name:str=None, score:"dict[str, dict[str, str|None]]"=None,
                 pickups:"list[int]"=None, drops:"list[int]"=None, defenses:"list[int]"=None, charge_state:str=None, comments:"list[str]"=None, submission_time:int=None,
                 navigation_start:int=None, navigation_prematch:int=None, navigation_match:int=None, navigation_result:int=None, navigation_finish:int=None):
        self.version = version
        self.team_number = team_number
        self.match_number = match_number
        self.id = self._construct_id()
        self.scouter_name = scouter_name
        self.score = score
        self.pickups = pickups
        self.drops = drops
        self.defenses = defenses
        self.charge_state = charge_state
        self.comments = comments
        self.submission_time = submission_time
        #navigation timestamps
        self.navigation_start = navigation_start
        self.navigation_prematch = navigation_prematch
        self.navigation_match = navigation_match
        self.navigation_result = navigation_result
        self.navigation_finish = navigation_finish

    def __getitem__(self, key:str): return self.__dict__[key]
    def __setitem__(self, key:str, value): self.__dict__[key] = value
    def __contains__(self, key:str): return key in self.__dict__

    def __repr__(self):
        return f"<MatchData {self.id} from '{self.scouter_name}' at {hex(id(self))}>"

    def _construct_id(self)->int:
        if not (isinstance(self.team_number, int) and isinstance(self.match_number, int)):
            raise TypeError("MatchData team number and match number must both be of type int to generate a MatchData id.")
        #":04" will ensure that match number takes up at least 4 digits of space in the id, any untaken space is replaced with leading 0s
        return int(f"{self.team_number}{self.match_number:04}")

    #construction methods
    def construct_score_events(self)->"list[Event]":
        if self.score is None:
            raise KeyError(ContentKeys.SCORE)
        events = []
        for index, history in self.score.items():
            for timestamp, game_piece in history.items():
                events.append(Event(
                    EventActions.SCORE,
                    timestamp,
                    self.team_number,
                    self.match_number,
                    self.scouter_name,
                    index=int(index),
                    piece=game_piece
                ))
        return events

    def construct_drop_events(self)->"list[Event]":
        if self.drops is None:
            raise KeyError(ContentKeys.DROPS)
        return [Event(EventActions.DROP, timestamp, self.team_number, self.match_number, self.scouter_name) for timestamp in self.drops]

    def contruct_defense_events(self)->"list[Event]":
        if self.defenses is None:
            raise KeyError(ContentKeys.DEFENSES)
        return [Event(EventActions.DEFENSE, timestamp, self.team_number, self.match_number, self.scouter_name) for timestamp in self.defenses]

    def construct_pickup_events(self)->"list[Event]":
        if self.pickups is None:
            raise KeyError(ContentKeys.PICKUPS)
        return [Event(EventActions.PICK_UP, timestamp, self.team_number, self.match_number, self.scouter_name) for timestamp in self.pickups]


class Event(db.Model):
    __bind_key__ = BIND_KEY
    __tablename__ = TableNames.Event

    time = db.Column("time", Datetime, primary_key=True)
    action = db.Column("action", db.String, nullable=False)
    team_number = db.Column("team_number", db.Integer, nullable=False)
    match_number = db.Column("match_number", db.Integer, nullable=False)
    scouter_name = db.Column("scouter_name", db.String)
    other = db.Column("other", Json, nullable=False)

    @staticmethod
    def get(time:int)->"Event|None":
        "Query for the Event object by timestamp."
        return filter_search(Event, time=time).first()

    @staticmethod
    def search(**by):
        "Query for the Event object by the given criteria."
        return filter_search(Event, by)

    "Object representing an event that happened during the match."
    def __init__(self, action:str, time:datetime, team_number:int, match_number:int, scouter_name:str, **other):
        self.action = action
        self.time = time if isinstance(time, datetime) else from_utc_timestamp(time)
        #reference fields: can be used in database subclass to access the related objects
        self.team_number = team_number
        self.match_number = match_number
        self.scouter_name = scouter_name
        self.other = other
    
    def __getitem__(self, key:str): return self._other[key]
    def __setitem__(self, key:str, value): self._other[key] = value

    def __repr__(self):
        return f"<Event '{self.action}' : {to_utc_timestamp(self.time) or '-'} at {hex(id(self))}>"

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



class Match(db.Model):
    __bind_key__ = BIND_KEY
    __tablename__ = TableNames.Match

    number = db.Column("number", db.Integer, primary_key=True)
    teams = db.Column("teams", Json, nullable=False)
    events = db.Column("events", Json, nullable=False)

    @staticmethod
    def get(id:int)->"Match|None":
        "Query for the Match object by number."
        return filter_search(Match, id=id).first()

    @staticmethod
    def search(**by):
        "Query for the Match object by the given criteria."
        return filter_search(Match, by)

    def __init__(self, number:int, teams:"list[int]", events:"list[int]"):
        self.number = number
        self.teams = teams
        self.events = events

    def generate_report(self):
        team_match_reports = [TeamMatchReport(number, self.number) for number in self.teams]
        #TODO create MatchReport from TeamMatchReport objects


class Scouter(db.Model):
    __bind_key__ = BIND_KEY
    __tablename__ = TableNames.Scouter

    name = db.Column("name", db.String, primary_key=True)
    year = db.Column("year", db.Integer, nullable=True)
    submissions = db.Column("submissions", Json, nullable=False)

    def __init__(self, name:str, year:int, submissions:"list[int]"):
        self.name = name
        self.year = year
        self.submissions = submissions

class ScoreGroup:
    def __init__(self, pickup:"Event|None"=None, drop:"Event|None"=None, score:"Event|None"=None, ammend=False):
        if not (drop is None or score is None) or drop is score:
            raise ValueError("ScoreGroup must contain either drop Event or score Event, not both or neither.")
        self.pickup = pickup
        self.drop = drop
        self.score = score
        self.ammend = ammend #if this event ammends a score event made in this node previously
        self._get_node_location()

    def __contains__(self, value):
        return value is not None and value in (self.pickup, self.second)
        
    def __len__(self):
        return self.has_first+1 #0+1 or 1+1

    def __getitem__(self, index:int):
        return (self.first, self.second)[index]

    def __setitem__(self, index:int, value):
        if index is 0:
            self.first = value
        elif index is 1:
            self.second = value
        else:
            raise IndexError("ScoreGroup assignment index out of range.")
    
    def __iter__(self):
        yield self.first
        yield self.second

    @property
    def first(self)->Event: return self.pickup
    @first.setter
    def first(self, value:Event):
        if not (isinstance(value, Event) or value is None):
            raise TypeError(f"ScoreGroup first element must be Event instance, got {type(value).__name__}.")
        self.pickup = value

    @property
    def second(self)->Event: return self.drop or self.score
    @second.setter
    def second(self, value:Event):
        if not isinstance(value, Event):
            raise TypeError(f"ScoreGroup second element must be Event instance, got {type(value).__name__}.")
        if self.drop is not None:
            self.drop = value
        else:
            self.score = value

    @property
    def has_first(self): return self.pickup is not None
    @property
    def delta(self)->timedelta: return self.second.time-self.pickup.time
    @property
    def index(self)->int: return self._index
    @property
    def row(self)->int: return self._row
    @property
    def column(self)->int: return self._column

    def _get_node_location(self):
        self._index = (int(self.score.other["index"]) if "index" in self.score.other else None) if self.score is not None else None
        self._row = int(self._index / 9)
        self._column = self._index % 9 if self._index is not None else None

    def get_score(self):
        raise NotImplementedError("TODO determine the points (regular & ranking) gained from this action, or 0 if dropped")


class TeamMatchReport:
    "An object representing what a team did in a match based on Events. Should not be used to mutate or modify database contents, just for analytics."

    def __init__(self, team_number:int, match_number:int):
        self.team_number = team_number
        self.match_number = match_number
        #all events
        self.events:"list[Event]" = list(Event.search(team_number=team_number, match_number=match_number))
        self.events.sort()
        #event categories
        self.pickups = []
        self.drops = []
        self.scores = []
        self.end_auto:Event = None #event that marks the end of auto
        self.score_groups:"list[ScoreGroup]" = []

    def add_events(self, *events:"list[Event|int]"):
        "Add events to the score grid."
        for event in events:
            if isinstance(event, Event) and event not in self.events:
                to_add = event
            elif isinstance(event, int):
                e = Event.get(event)
                if e is None or e in self.events:
                    continue
                to_add = e
            else: continue

            if to_add.team_number==self.team_number and to_add.match_number==self.match_number:
                self.events.append(to_add)
        self.events.sort()

    def before_auto(self, event:Event):
        return event.time < self.end_auto.time

    def categorize_events(self):
        "Categorize events by action, timestamp, and other things."
        #TODO categorize based on action self.pickups = [...]; self.drops = [...]; ...
        ...
        #TODO find the auto_end/teleop_start event and split events into auto and teleop lists
        ...
        self._get_score_groups()
        #TODO get navigational events (scout_start:home.html, prematch_start:prematch.html, match_start:scout.html, result_start:result.html, scout_finish:qrscanner.html)
        ...
        #TODO autogenerate self.end_auto event at 15 seconds from scout.html start timestamp if its missing in self.events, else set

    def _get_score_groups(self):
        "Group each pickup event with a score or drop event.\nIf there is no pickup event to go with the found score or drop event, thescore/drop event is put into a ScoreGroup on its own."
        search_start = 0
        f_si, f_se = self._find_event(EventActions.SCORE, search_start)
        f_di, f_de = self._find_event(EventActions.DROP, search_start)
        s_index, second = None, None
        while f_si != -1 and f_di != -1:
            s_index, second = (f_si, f_se) if f_si < f_di and f_si > -1 else (f_di, f_de) #get which one is first
            f_pi, f_pe = self._find_event(EventActions.PICK_UP, search_start, s_index)
            self.score_groups.append(ScoreGroup(f_pe, drop=f_de if second is f_de else None, score=f_se if f_se is second else None))
            #get next group
            search_start = s_index+1
            f_si, f_se = self._find_event(EventActions.SCORE, search_start)
            f_di, f_de = self._find_event(EventActions.DROP, search_start)

    def _find_event(self, action:str, search_start=0, end_index=...)->"tuple[int, Event]":
        if end_index is ...:
            end_index = len(self.events)
        for i, event in enumerate(self.events[search_start:end_index]):
            if event.action == action:
                return i+search_start, event
        return -1, None

class Team:
    "A FRC Team. Team-specific data is gotten from The Blue Alliance API instead of being stored locally." #NOTE: this may change :)
    def __init__(self, number:int):
        self.number = number

    def get_matches(self, **filter)->"list[Match]":
        return [match for match in (Match.search(**filter) if filter else get_all(Match)) if self.number in match.teams]

    def get_submissions(self, **filter)->"list[MatchData]":
        return list(MatchData.search(**dict(filter, team_number=self.number)))

#data querying
def filter_search(model:type, search:"dict[str]"):
    "Query for a given model with the given search requirements."
    q:sqlalchemy.orm.Query = db.session.query(model)
    return q.filter_by(**search)

def get_all(model:type):
    "Get all rows of a given model as objects."
    q:sqlalchemy.orm.Query = db.session.query(model)
    return q.all()

#functions
def map_index_to_type(index:int)->str:
    "Given index, get its score node type in the score grid."
    if isinstance(index, int) and (index >= 0 or index < 27):
        for indexes, type in zip(SCORE_GRID_INDEX, SCORE_GRID_NAMES):
            if index in indexes:
                return type
    raise IndexError("Index out of range.")

def map_index_to_node_row(index:int):
    "Given index, get its score grid row."
    if isinstance(index, int) and (index >= 0 or index < 27):
        for indexes, row in zip(SCORE_GRID_ROW_INDEX, SCORE_GRID_ROW_NAMES):
            if index in indexes:
                return row
    raise IndexError("Index out of range.")

def from_utc_timestamp(value:int)->datetime: #assuming that value is a javascript timestamp in ms since python takes timestamp in seconds
    return datetime.fromtimestamp(value/1000, tz=timezone.utc).astimezone(LOCAL_TIMEZONE)

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
        return MatchData.generate(fields)
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