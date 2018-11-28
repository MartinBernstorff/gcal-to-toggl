from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from task_dicts import calendar_exclude

########################
# Baseline established #
########################
# Get calendar events
# If modifying these scopes, delete the file token.json.
def init(index_formatted, day_after_index_formatted):
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

    global event_list

    event_list = []

    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Get all calendars
    calendar_list = service.calendarList().list().execute()

    for calendar_list_entry in calendar_list['items']:
        if calendar_list_entry["summary"] in calendar_exclude:
            continue
        else:
            events_result = service.events().list(calendarId=calendar_list_entry["id"],
                                                  timeMin=index_formatted,
                                                  timeMax=day_after_index_formatted,
                                                  singleEvents=True,
                                                  orderBy='startTime').execute()
            events = events_result.get('items', [])

            i = 0 # Skip first Sleep event

            for event in events:
                if event["summary"] == "Sleep":
                    if i == 0:
                        i = i + 1
                        continue
                if "dateTime" in event['start'] and "dateTime" in event['end']:
                    event_list.append([event['summary'],
                                       event['start']['dateTime'],
                                       event['end']['dateTime']
                                       ])


    event_list.sort(key=lambda x: x[1])
