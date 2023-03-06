from .constants import *
from datetime import datetime, timedelta, timezone
import json
from PIL import Image
from pyzbar import pyzbar
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

class Points:
    __slots__ = "value", "type"

    def __init__(self, value:int, type:str):
        self.value = value
        self.type = type

    def __int__(self): return self.value

    def __add__(self, value):
        if isinstance(value, Points):
            if self.type != value.type:
                raise ValueError("Point types must be the same to add.")
            return Points(self.value+value.value, self.type)
        else:
            return Points(self.value+value, self.type)
        
    def __sub__(self, value):
        if isinstance(value, Points):
            if self.type != value.type:
                raise ValueError("Point types must be the same to subtract.")
            return Points(self.value-value.value, self.type)
        else:
            return Points(self.value-value, self.type)
        
    def __mul__(self, value):
        if isinstance(value, Points):
            if self.type != value.type:
                raise ValueError("Point types must be the same to multiply.")
            return Points(self.value*value.value, self.type)
        else:
            return Points(self.value*value, self.type)
        
    def __truediv__(self, value):
        if isinstance(value, Points):
            if self.type != value.type:
                raise ValueError("Point types must be the same to divide.")
            return Points(int(self.value/value.value), self.type)
        else:
            return Points(int(self.value/value), self.type)
        
    def __floordiv__(self, value):
        if isinstance(value, Points):
            if self.type != value.type:
                raise ValueError("Point types must be the same to divide.")
            return Points(self.value//value.value, self.type)
        else:
            return Points(self.value//value, self.type)
        
    def __eq__(self, value):
        if isinstance(value, Points):
            return self.value == value.value and self.type == value.type
        else:
            return super().__eq__(value)
        
    def __gt__(self, value):
        if isinstance(value, Points):
            return self.value > value.value and self.type > value.type
        else:
            return super().__eq__(value)
        
    def __lt__(self, value):
        if isinstance(value, Points):
            return self.value < value.value and self.type < value.type
        else:
            return super().__eq__(value)






    # @classmethod
    # def generate(cls, data:dict):
    #     "Create a MatchData object from raw data."
    #     preliminary_data = data.get(ContentKeys.PRELIMINARY_DATA,{})
    #     nav_stamps = data.get(ContentKeys.NAV_STAMPS,{})
    #     return cls(
    #         version=data.get(ContentKeys.VERSION),
    #         team_number=preliminary_data.get(ContentKeys.TEAM_NUMBER),
    #         match_number=preliminary_data.get(ContentKeys.MATCH_NUMBER),
    #         scouter_name=preliminary_data.get(ContentKeys.SCOUTER_NAME),
    #         score=data.get(ContentKeys.SCORE),
    #         pickups=data.get(ContentKeys.PICKUPS),
    #         drops=data.get(ContentKeys.DROPS),
    #         defenses=data.get(ContentKeys.DEFENSES),
    #         charge_state=data.get(ContentKeys.CHARGE_STATE),
    #         comments=data.get(ContentKeys.COMMENTS),
    #         end_auto=data.get(ContentKeys.END_AUTO),
    #         navigation_start=nav_stamps.get("home.html"),
    #         navigation_prematch=nav_stamps.get("prematch.html"),
    #         navigation_match=nav_stamps.get("scout.html"),
    #         navigation_result=nav_stamps.get("result.html"),
    #         navigation_finish=nav_stamps.get("qrscanner.html")

    #construction methods
    # def construct_score_events(self)->"list[Event]":
    #     if self.score is None:
    #         raise KeyError(ContentKeys.SCORE)
    #     events = []
    #     for index, history in self.score.items():
    #         for timestamp, game_piece in history.items():
    #             events.append(Event(
    #                 EventActions.SCORE,
    #                 timestamp,
    #                 self.team_number,
    #                 self.match_number,
    #                 self.scouter_name,
    #                 index=int(index),
    #                 piece=game_piece
    #             ))
    #     return events

    # def construct_drop_events(self)->"list[Event]":
    #     if self.drops is None:
    #         raise KeyError(ContentKeys.DROPS)
    #     return [Event(EventActions.DROP, timestamp, self.team_number, self.match_number, self.scouter_name) for timestamp in self.drops]

    # def contruct_defense_events(self)->"list[Event]":
    #     if self.defenses is None:
    #         raise KeyError(ContentKeys.DEFENSES)
    #     return [Event(EventActions.DEFENSE, timestamp, self.team_number, self.match_number, self.scouter_name) for timestamp in self.defenses]

    # def construct_pickup_events(self)->"list[Event]":
    #     if self.pickups is None:
    #         raise KeyError(ContentKeys.PICKUPS)
    #     return [Event(EventActions.PICK_UP, timestamp, self.team_number, self.match_number, self.scouter_name) for timestamp in self.pickups]

    # def construct_events(self)->"list[Event]":
    #     for e in self.construct_drop_events():
    #         yield e
    #     for e in self.contruct_defense_events():
    #         yield e
    #     for e in self.construct_pickup_events():
    #         yield e
    #     yield Event(EventActions.END_AUTO, self.end_auto, self.team_number, self.match_number, self.scouter_name)
    #     yield Event(EventActions.START, self.navigation_match, self.team_number, self.match_number, self.scouter_name)
    #     yield Event(EventActions.END, self.navigation_result, self.team_number, self.match_number, self.scouter_name)


class Event:
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
        if index == 0:
            self.first = value
        elif index == 1:
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
        for row, points in SCORE_VALUE_INDEX.items():
            if self.row in row:
                return points
        return 0


#TODO make this into a function for processing some of the raw data into more usable values: list[Event] -> list[ScoreGroup] -> (cubes_places:int, cones_placed:int, ...)
class TeamMatchReport:
    "An object representing what a team did in a match based on Events and other match data. Should not be used to mutate or modify database contents, just for analytics."

    def __init__(self, team_number:int, match_number:int):
        self._init = False
        self.team_number = team_number
        self.match_number = match_number
        #match_data = MatchData.get(MatchData._construct_id(team_number, match_number))
        #all events
        self.events:"list[Event]" = list(Event.search(team_number=team_number, match_number=match_number))
        self.events.sort()
        #event categories
        self.event_categories:"dict[str, list[Event]]" = {
            EventActions.PICK_UP:[],
            EventActions.DROP:[],
            EventActions.SCORE:[],
            EventActions.DEFENSE:[]
        }
        self.started:Event = None
        self.ended:Event = None
        self.end_auto:Event = None #event that marks the end of auto
        self.score_groups:"list[ScoreGroup]" = []
        self.links:"list[tuple[ScoreGroup, ScoreGroup, ScoreGroup]]" = []
        self.events_auto = []
        self.events_teleop = []
        self.score_deltas = []
        #as seen on manual 6.4.3 (pg 46) {Award Name: value}
        #TODO cooperation bonus requires both alliances to do 3, so thats a MatchReport thing (boolean)
        self.points_auto:"dict[str, int]" = {
            ScoreAwardName.MOBILITY:0,
            ScoreAwardName.GAME_PIECES:0,
            #TODO have docked and engaged points calculated in AllianceMatchReport (depends on stats of multiple team reports)
        }
        self.points_teleop:"dict[str, int]" = {
            ScoreAwardName.GAME_PIECES:0,
            ScoreAwardName.LINK:0,
            ScoreAwardName.PARK:0
        }
        self.points_ranking:"dict[str, int]" = {
            ScoreAwardName.SUSTAINABILITY:0,
            ScoreAwardName.ACTIVATION:0 #TODO figure out how this is earned, because one team can not earn 26 charging station points alone
            #TODO Tie and Win go in the AllianceMatchReport
        }

    def before_teleop(self, event:Event)->bool:
        return event.time < self.end_auto.time
    
    def initialize_report(self):
        if self._init: return
        self._init = True
        self._categorize_events()
        self._get_score_groups()
        self._get_score_links()
        self._get_score_deltas()
        self._get_points()

    def _categorize_events(self):
        "Categorize events by action, timestamp, and other things."
        #sort based on action name
        for event in self.events:
            if event.action in self.event_categories:
                self.event_categories[event.action].append(event)
            elif not self.started and event.action == EventActions.START:
                self.started = event
            elif not self.ended and event.action == EventActions.END:
                self.ended = event
        #find the auto_end/teleop_start event and split events into auto and teleop lists
        for i, event in enumerate(self.events):
            if event.action == EventActions.END_AUTO:
                self.end_auto = event
                self.events_auto = self.events[:i]
                self.events_teleop = self.events[i+1:]
                break
        else: #TODO autogenerate self.end_auto event at 15 seconds from scout.html start timestamp if its missing in self.events, else set
            self.end_auto = Event(EventActions.END_AUTO, self.started.time+timedelta(seconds=15), self.started.team_number, self.started.match_number, self.started.scouter_name)
            for i, event in enumerate(self.events):
                if event.time < self.end_auto.time:
                    self.events_auto.append(event)
                elif event.time >= self.end_auto.time:
                    self.events_teleop = self.events[i:]
                    break


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

    def _get_score_links(self):
        for irow in range(len(SCORE_GRID_ROW_INDEX)): #0, 1, 2
            current_link:"list[ScoreGroup]" = []
            for sg in self.score_groups:
                if not (sg.score and sg.row == irow):
                    continue
                elif not current_link or sg.index == current_link[-1].index+1: #sg is first in link or sg is right after last
                    current_link.append(sg)
                else:
                    current_link = [sg] #the current link starts with this sg

                if len(current_link)==3:
                    self.links.append(tuple(current_link))
                    current_link.clear()

    def _get_score_deltas(self):
        self.score_deltas = []
        for sg in self.score_groups:
            if not sg.score:
                continue
            self.score_deltas.append(sg.second.time-sg.first.time)

    def _get_points(self):
        for sg in self.score_groups:
            if not sg.score:
                continue
            if self.before_teleop(sg.second):
                self.points_auto[ScoreAwardName.GAME_PIECES] += sg.score+1
            else:
                self.points_teleop[ScoreAwardName.GAME_PIECES] += sg.score

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



# def _debug(path:str): #debug used in scouting app presentation on 2/4/2023
#     from pprint import pprint
#     print("="*10+"RAW DATA"+"="*10)
#     pprint(parse_qr_code(path))
#     data:MatchData = load_qr_code(path)
#     print("\n"+"="*10+"EXTRACTED DATA"+"="*10)
#     for attr, value in data.items():
#         print(attr+":",value)
#     for attr, value in MatchData.__dict__.items():
#         if isinstance(value, property):
#             print(attr+":", getattr(data, attr))