from .constants import *
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
import json
from PIL import Image
from pyzbar import pyzbar

with open(API_KEYS_FILE) as f:
    KEYS = json.load(f)
SHEETS_OAUTH_DATA = KEYS[SHEETS_OAUTH]

#NOTE: the notes below are about scoring, points, etc
#cite: see manual 6.4:44-45 for time period between action taking place and when it counts for points
#cite: see manual 6.4.1:45 for scoring criteria
#cite: see manual 6.4.3:46-47 for point values

#cite: https://stackoverflow.com/a/43587551


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

    # def contruct_defense_events(self)->"list[Event]":
    #     if self.defenses is None:
    #         raise KeyError(ContentKeys.DEFENSES)
    #     return [Event(EventActions.DEFENSE, timestamp, self.team_number, self.match_number, self.scouter_name) for timestamp in self.defenses]

@dataclass(slots=True)
class Data:
    "Data that gets put into google sheets."

    team_number:int
    match_number:int
    scouter:str
    cones_bottom:int
    cones_middle:int
    cones_top:int
    cubes_bottom:int
    cubes_middle:int
    cubes_top:int
    picked_up_ground:int
    picked_up_shelf:int
    drops:int
    charging_pad_auto:str
    charging_pad_teleop:str
    defenses:int
    min_score_delta:float
    max_score_delta:float
    avg_score_delta:float
    auto_activity:float
    teleop_activity:float
    comments:str


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


# class TeamMatchReport:
#     "An object representing what a team did in a match based on Events and other match data. Should not be used to mutate or modify database contents, just for analytics."

#     def __init__(self, team_number:int, match_number:int):
#         self._init = False
#         self.team_number = team_number
#         self.match_number = match_number
#         #match_data = MatchData.get(MatchData._construct_id(team_number, match_number))
#         #all events
#         self.events:"list[Event]" = list(Event.search(team_number=team_number, match_number=match_number))
#         self.events.sort()
#         #event categories
#         self.event_categories:"dict[str, list[Event]]" = {
#             EventActions.PICK_UP:[],
#             EventActions.DROP:[],
#             EventActions.SCORE:[],
#             EventActions.DEFENSE:[]
#         }
#         self.started:Event = None
#         self.ended:Event = None
#         self.end_auto:Event = None #event that marks the end of auto
#         self.score_groups:"list[ScoreGroup]" = []
#         self.links:"list[tuple[ScoreGroup, ScoreGroup, ScoreGroup]]" = []
#         self.events_auto = []
#         self.events_teleop = []
#         self.score_deltas = []
#         #as seen on manual 6.4.3 (pg 46) {Award Name: value}
#         # cooperation bonus requires both alliances to do 3, so thats a MatchReport thing (boolean)
#         self.points_auto:"dict[str, int]" = {
#             ScoreAwardName.MOBILITY:0,
#             ScoreAwardName.GAME_PIECES:0,
#             # have docked and engaged points calculated in AllianceMatchReport (depends on stats of multiple team reports)
#         }
#         self.points_teleop:"dict[str, int]" = {
#             ScoreAwardName.GAME_PIECES:0,
#             ScoreAwardName.LINK:0,
#             ScoreAwardName.PARK:0
#         }
#         self.points_ranking:"dict[str, int]" = {
#             ScoreAwardName.SUSTAINABILITY:0,
#             ScoreAwardName.ACTIVATION:0 # figure out how this is earned, because one team can not earn 26 charging station points alone
#             # Tie and Win go in the AllianceMatchReport
#         }

#     def before_teleop(self, event:Event)->bool:
#         return event.time < self.end_auto.time

#     def initialize_report(self):
#         if self._init: return
#         self._init = True
#         self._categorize_events()
#         self._get_score_groups()
#         self._get_score_links()
#         self._get_score_deltas()
#         self._get_points()

#     def _categorize_events(self):
#         "Categorize events by action, timestamp, and other things."
#         #sort based on action name
#         for event in self.events:
#             if event.action in self.event_categories:
#                 self.event_categories[event.action].append(event)
#             elif not self.started and event.action == EventActions.START:
#                 self.started = event
#             elif not self.ended and event.action == EventActions.END:
#                 self.ended = event
#         #find the auto_end/teleop_start event and split events into auto and teleop lists
#         for i, event in enumerate(self.events):
#             if event.action == EventActions.END_AUTO:
#                 self.end_auto = event
#                 self.events_auto = self.events[:i]
#                 self.events_teleop = self.events[i+1:]
#                 break
#         else: # autogenerate self.end_auto event at 15 seconds from scout.html start timestamp if its missing in self.events, else set
#             self.end_auto = Event(EventActions.END_AUTO, self.started.time+timedelta(seconds=15), self.started.team_number, self.started.match_number, self.started.scouter_name)
#             for i, event in enumerate(self.events):
#                 if event.time < self.end_auto.time:
#                     self.events_auto.append(event)
#                 elif event.time >= self.end_auto.time:
#                     self.events_teleop = self.events[i:]
#                     break

#     def _get_score_links(self):
#         for irow in range(len(SCORE_GRID_ROW_INDEX)): #0, 1, 2
#             current_link:"list[ScoreGroup]" = []
#             for sg in self.score_groups:
#                 if not (sg.score and sg.row == irow):
#                     continue
#                 elif not current_link or sg.index == current_link[-1].index+1: #sg is first in link or sg is right after last
#                     current_link.append(sg)
#                 else:
#                     current_link = [sg] #the current link starts with this sg

#                 if len(current_link)==3:
#                     self.links.append(tuple(current_link))
#                     current_link.clear()

#     def _get_points(self):
#         for sg in self.score_groups:
#             if not sg.score:
#                 continue
#             if self.before_teleop(sg.second):
#                 self.points_auto[ScoreAwardName.GAME_PIECES] += sg.score+1
#             else:
#                 self.points_teleop[ScoreAwardName.GAME_PIECES] += sg.score

#functions

def _find_event(events:"list[Event]", actions:"tuple[str]", search_start=0, end_index=...)->"tuple[int, Event]":
    if end_index is ...:
        end_index = len(events)
    for i, event in enumerate(events[search_start:end_index]):
        if event.action in actions:
            return i+search_start, event #enumeration happens over slice, add i+search_start gets index in the entire list
    return -1, None

def _get_score_groups(events:"list[Event]"):
    "Group each pickup event with a score or drop event.\nIf there is no pickup event to go with the found score or drop event, thescore/drop event is put into a ScoreGroup on its own."
    score_groups:"list[ScoreGroup]" = []
    indexes = set()

    search_start = 0
    #get index and object of first score/drop event
    s_index, second = _find_event((EventActions.SCORE, EventActions.DROP), search_start)
    while s_index != -1:
        #get pickup event
        f_pi, f_pe = _find_event((EventActions.PICK_UP), search_start, s_index)
        drop = second if second is not None and second.action == EventActions.DROP else None
        score_index = second.index if drop is None else None
        score_groups.append(ScoreGroup(f_pe, drop=drop, score=second if drop is None else None, ammend=score_index in indexes))
        if score_index is not None:
            indexes.add(score_index)
        #get next group
        search_start = s_index+1
        s_index, second = _find_event((EventActions.PICK_UP, EventActions.DROP), search_start)
    return score_groups

def _get_score_deltas(score_groups:"list[ScoreGroup]")->"list[timedelta]":
    score_deltas = []
    for sg in score_groups:
        if not sg.score:
            continue
        score_deltas.append(sg.second.time-sg.first.time)
    return score_deltas

def construct_events(raw:"dict[str]"):
    team_number = raw.get(ContentKeys.TEAM_NUMBER)
    match_number = raw.get(ContentKeys.MATCH_NUMBER)
    scouter_name = raw.get(ContentKeys.SCOUTER_NAME)
    for index, history in raw.get(ContentKeys.SCORE,{}).items():
        for timestamp, game_piece in history.items():
            yield Event(
                EventActions.SCORE,
                timestamp,
                team_number,
                match_number,
                scouter_name,
                index=int(index),
                piece=game_piece
            )

    for timestamp in raw.get(ContentKeys.DROPS,()):
        yield Event(EventActions.DROP, timestamp, team_number, match_number, scouter_name)
    for timestamp in raw.get(ContentKeys.PICKUPS,()):
        yield Event(EventActions.PICK_UP, timestamp, team_number, match_number, scouter_name)
    for timestamp in raw.get(ContentKeys.SHELF_PICKUPS,()):
        yield Event(EventActions.PICK_UP_SHELF, timestamp, team_number, match_number, scouter_name)
    for timestamp in raw.get(ContentKeys.DEFENSES, ()):
        yield Event(EventActions.DEFENSE, timestamp, team_number, match_number, scouter_name)

def process_events(events:"list[Event]")->"dict[str]":
    #cones&cubes bottom,middle,top; min,max,avg score delta
    score_groups = _get_score_groups(events)
    deltas = _get_score_deltas(score_groups)

    rows = [] #top, middle, bottom
    for row_range in SCORE_GRID_ROW_INDEX:
        rows.append([event for event in events if event.action==EventActions.SCORE and event.index in row_range]) #get scores in top, middle, bottom respectively

    return {
        "cones_bottom":len([event for event in rows[2] if event.piece==GamePiece.CONE]),
        "cones_middle":len([event for event in rows[1] if event.piece==GamePiece.CONE]),
        "cones_top":len([event for event in rows[0] if event.piece==GamePiece.CONE]),
        "cubes_bottom":len([event for event in rows[2] if event.piece==GamePiece.CUBE]),
        "cubes_middle":len([event for event in rows[1] if event.piece==GamePiece.CUBE]),
        "cubes_top":len([event for event in rows[0] if event.piece==GamePiece.CUBE]),
        "min_score_delta":round(min(deltas).total_seconds(), 3),
        "max_score_delta":round(max(deltas).total_seconds(), 3),
        "avg_score_delta":round(sum(delta.total_seconds() for delta in deltas)/len(deltas), 3)
    }

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
    return int(dt.astimezone(timezone.utc).timestamp()*1000) #from f"{seconds}.{microseconds}" -> milliseconds

def parse_qr_code(fp)->"dict[str]":
    "Parse the qr code and extract the JSON data"
    decoded:list = pyzbar.decode(Image.open(fp))
    return json.loads(decoded[0].data.decode("ascii"))

def handle_upload(raw:"dict[str]"):
    "Handle data sent to the upload route"
    data = process_data(raw)
    save_local(raw)
    save_to_sheets(data)

def process_data(raw:"dict[str]")->Data:
    "Turn raw gathered data into Data for each column in google sheets."
    preliminary_data = raw.get(ContentKeys.PRELIMINARY_DATA) or {}

    nav_stamps = raw.get(ContentKeys.NAV_STAMPS) or {}
    navigation_match = nav_stamps.get("scout.html")

    end_auto = raw.get(ContentKeys.END_AUTO)
    if end_auto is not None:
        end_auto = from_utc_timestamp(end_auto)
    elif navigation_match:
        end_auto:datetime = navigation_match+timedelta(seconds=15)


    #NOT NEEDED (i don't think)
    #
    #
    # navigation_start = nav_stamps.get("home.html")
    # navigation_prematch = nav_stamps.get("prematch.html")
    # navigation_result = nav_stamps.get("result.html")
    # navigation_finish = nav_stamps.get("qrscanner.html")

    events = list(construct_events(raw))
    events.sort(key=lambda e: e.time)

    processed = process_events(events)

    return Data(
            team_number=preliminary_data.get(ContentKeys.TEAM_NUMBER),
            match_number=preliminary_data.get(ContentKeys.MATCH_NUMBER),
            scouter=preliminary_data.get(ContentKeys.SCOUTER_NAME),
            cones_bottom=processed["cones_bottom"],
            cones_middle=processed["cones_middle"],
            cones_top=processed["cones_top"],
            cubes_bottom=processed["cubes_bottom"],
            cubes_middle=processed["cubes_middle"],
            cubes_top=processed["cubes_top"],
            picked_up_ground=len(raw.get(ContentKeys.PICKUPS, ())),
            picked_up_shelf=len(raw.get(ContentKeys.SHELF_PICKUPS, ())),
            drops=len(raw.get(ContentKeys.DROPS, ())),
            charging_pad_auto=raw.get(ContentKeys.CHARGE_STATE_AUTO),
            charging_pad_teleop=raw.get(ContentKeys.CHARGE_STATE),
            defenses=len(raw.get(ContentKeys.DEFENSES, ())),
            min_score_delta=processed["min_score_delta"],
            max_score_delta=processed["max_score_delta"],
            avg_score_delta=processed["avg_score_delta"],
            auto_activity=len([event for event in events if event.time < end_auto]) if end_auto else None,
            teleop_activity=len([event for event in events if event.time > end_auto]) if end_auto else None,
            comments=raw.get(ContentKeys.COMMENTS)
    )

def get_sheets_api_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(SHEETS_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(SHEETS_TOKEN_FILE, SHEETS_SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(SHEETS_OAUTH_DATA, SHEETS_SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(SHEETS_TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return creds

def get_sheet_columns()->list:
    "Get columns for the google sheets."

    creds = get_sheets_api_creds()

    try:
        service:Resource = build("sheets", "v4", credentials=creds)
        sheets:Resource = service.spreadsheets()
        data = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="'Backup Data'!A1:1").execute()
        return data["values"][0] if "values" in data else []
    except HttpError as e:
        print(e)
    finally:
        if "service" in locals():
            service.close()

sheet_columns = get_sheet_columns()

def save_to_sheets(data:Data):
    "Save processed data to the google sheets."

    creds = get_sheets_api_creds()

    try:
        insert_range = "A2:A" #range to insert into
        service:Resource = build("sheets", "v4", credentials=creds)
        sheets:Resource = service.spreadsheets()
        #TODO implement a queue system (depending on the api rate limits) where multiple rows are inserted in one request.
        # A stress test & other research would be required to determine the necessity of this
        row = [getattr(data, SHEETS_COLUMN_NAMES[column]) if column in SHEETS_COLUMN_NAMES else "" for column in sheet_columns]
        #insert data at the end of the Data sheet
        print(sheets.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"Data!{insert_range}",
            valueInputOption="RAW", insertDataOption="INSERT_ROWS", body={"values":[row]}
        ).execute())
        #insert data at the end of the Backup Data sheet
        print(sheets.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'Backup Data'!{insert_range}",
            valueInputOption="RAW", insertDataOption="INSERT_ROWS", body={"values":[row]}
        ).execute())
    except HttpError as e:
        print(e)
    finally:
        if "service" in locals():
            service.close()

def save_local(raw:"dict[str]|str"):
    "Save (append) the raw data to a local file."
    if not isinstance(raw, str):
        raw = json.dumps(raw)
    with open(SUBMISSIONS_FILE, "a" if os.path.isfile(SUBMISSIONS_FILE) else "w") as f:
        f.write(raw+"\n")


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
