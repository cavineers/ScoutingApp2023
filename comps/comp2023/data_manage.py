from .constants import *
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
import json
# from PIL import Image
# from pyzbar import pyzbar

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
    date:str
    cones_bottom:int
    cones_middle:int
    cones_top:int
    cubes_bottom:int
    cubes_middle:int
    cubes_top:int
    cones_total:int
    cubes_total:int
    total_pieces:int
    cones_auto:int
    cubes_auto:int
    cones_teleop:int
    cubes_teleop:int
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
        self.time = time if isinstance(time, datetime) else from_utc_timestamp(float(time))
        #reference fields: can be used in database subclass to access the related objects
        self.team_number = team_number
        self.match_number = match_number
        self.scouter_name = scouter_name
        self.other = other

    def __getitem__(self, key:str): return self.other[key]
    def __setitem__(self, key:str, value): self.other[key] = value

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

def _get_score_deltas(events:"list[Event]")->"list[timedelta]":
    pickup = None
    score_deltas = []
    for event in events:
        if event.action in (EventActions.PICK_UP, EventActions.PICK_UP_SHELF):
            pickup = event
        elif event.action == EventActions.SCORE and pickup is not None:
            score_deltas.append(event.time-pickup.time)
        elif event.action == EventActions.DROP:
            pickup = None
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

def _get_unique_scores(score_range:"list[Event]", piece:str):
    s = set()
    for event in score_range:
        if event.other["piece"] == piece:
            s.add(event.other["index"])
        elif event.other["piece"] is None:
            s.discard(event.other["index"])
    return s

def process_events(events:"list[Event]")->"dict[str]":
    #cones&cubes bottom,middle,top; min,max,avg score delta
    deltas = _get_score_deltas(events)
    rows:"list[list[Event]]" = [] #top, middle, bottom
    for row_range in SCORE_GRID_ROW_INDEX:
        rows.append([event for event in events if event.action==EventActions.SCORE and event.other["index"] in row_range]) #get scores in top, middle, bottom respectively

    return {
        "cones_bottom":len(_get_unique_scores(rows[2], GamePiece.CONE)),
        "cones_middle":len(_get_unique_scores(rows[1], GamePiece.CONE)),
        "cones_top":len(_get_unique_scores(rows[0], GamePiece.CONE)),
        "cubes_bottom":len(_get_unique_scores(rows[2], GamePiece.CUBE)),
        "cubes_middle":len(_get_unique_scores(rows[1], GamePiece.CUBE)),
        "cubes_top":len(_get_unique_scores(rows[0], GamePiece.CUBE)),
        "min_score_delta":round(min(deltas).total_seconds(), 3) if deltas else 0,
        "max_score_delta":round(max(deltas).total_seconds(), 3) if deltas else 0,
        "avg_score_delta":round((sum(delta.total_seconds() for delta in deltas)/len(deltas)) if deltas else 0, 3)
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

# def parse_qr_code(fp)->"dict[str]":
#     "Parse the qr code and extract the JSON data"
#     decoded:list = pyzbar.decode(Image.open(fp))
#     return json.loads(decoded[0].data.decode("ascii"))

def handle_upload(raw:"dict[str]"):
    "Handle data sent to the upload route"
    raw[ContentKeys.DATE] = datetime.now().astimezone(timezone.utc).strftime("%m/%d")
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

    #get auto and teleop events
    auto_events:"list[Event]" = []
    teleop_events:"list[Event]" = []
    for event in events:
        if event.time<end_auto: auto_events.append(event)
        else: teleop_events.append(event)

    #fill in data
    return Data(
            team_number=preliminary_data.get(ContentKeys.TEAM_NUMBER),
            match_number=preliminary_data.get(ContentKeys.MATCH_NUMBER),
            scouter=preliminary_data.get(ContentKeys.SCOUTER_NAME),
            date=raw.get(ContentKeys.DATE),
            cones_bottom=processed["cones_bottom"],
            cones_middle=processed["cones_middle"],
            cones_top=processed["cones_top"],
            cubes_bottom=processed["cubes_bottom"],
            cubes_middle=processed["cubes_middle"],
            cubes_top=processed["cubes_top"],
            cones_total=sum((processed["cones_bottom"], processed["cones_middle"], processed["cones_top"])),
            cubes_total=sum((processed["cubes_bottom"], processed["cubes_middle"], processed["cubes_top"])),
            total_pieces=sum((processed["cones_bottom"], processed["cones_middle"], processed["cones_top"],
                             processed["cubes_bottom"], processed["cubes_middle"], processed["cubes_top"])),
            cones_auto=len(_get_unique_scores((event for event in auto_events if event.action == EventActions.SCORE), GamePiece.CONE)),
            cubes_auto=len(_get_unique_scores((event for event in auto_events if event.action == EventActions.SCORE), GamePiece.CUBE)),
            cones_teleop=len(_get_unique_scores((event for event in teleop_events if event.action == EventActions.SCORE), GamePiece.CONE)),
            cubes_teleop=len(_get_unique_scores((event for event in teleop_events if event.action == EventActions.SCORE), GamePiece.CUBE)),
            picked_up_ground=len(raw.get(ContentKeys.PICKUPS, ())),
            picked_up_shelf=len(raw.get(ContentKeys.SHELF_PICKUPS, ())),
            drops=len(raw.get(ContentKeys.DROPS, ())),
            charging_pad_auto=raw.get(ContentKeys.CHARGE_STATE_AUTO),
            charging_pad_teleop=raw.get(ContentKeys.CHARGE_STATE),
            defenses=len(raw.get(ContentKeys.DEFENSES, ())),
            min_score_delta=processed["min_score_delta"],
            max_score_delta=processed["max_score_delta"],
            avg_score_delta=processed["avg_score_delta"],
            auto_activity=len(auto_events) if end_auto else None,
            teleop_activity=len(teleop_events) if end_auto else None,
            comments="\n".join(raw.get(ContentKeys.COMMENTS, ()))
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

def save_to_sheets(*datas:Data):
    "Save processed data to the google sheets."

    creds = get_sheets_api_creds()

    try:
        insert_range = "A2:A" #range to insert into
        service:Resource = build("sheets", "v4", credentials=creds)
        sheets:Resource = service.spreadsheets()
        #TODO implement a queue system (depending on the api rate limits) where multiple rows are inserted in one request.
        # A stress test & other research would be required to determine the necessity of this
        rows = [[getattr(data, SHEETS_COLUMN_NAMES[column]) if column in SHEETS_COLUMN_NAMES else "" for column in sheet_columns] for data in datas]
        #insert data at the end of the Data sheet
        print(sheets.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"Data!{insert_range}",
            valueInputOption="RAW", insertDataOption="INSERT_ROWS", body={"values":rows}
        ).execute())
        #insert data at the end of the Backup Data sheet
        print(sheets.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'Backup Data'!{insert_range}",
            valueInputOption="RAW", insertDataOption="INSERT_ROWS", body={"values":rows}
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
