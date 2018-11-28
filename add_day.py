# Date and time improts
import datetime
import time
from datetime import datetime as dt

# Integration imports
from credentials import TOGGL_TOKEN, AIRTABLE_API_KEY
from toggl.TogglPy import Toggl
from airtable import Airtable
from airtable_integrations import make_dictionary_of_base
import gcal

#Utilities
from pprint import pprint
from task_dicts import event_exclude

toggl = Toggl()

toggl.setAPIKey(TOGGL_TOKEN)

#Generate today-string
index = dt.today() + datetime.timedelta(-1) #<--- Beware the time-delta!
index_midnight = index.replace(hour=0, minute=1)
index_formatted = index_midnight.isoformat() + 'Z'
index_str = dt.strftime(index,'%Y-%m-%d')

day_after_index = index + datetime.timedelta(1)
day_after_index_midnight = day_after_index.replace(hour=0, minute=1)
day_after_index_formatted = day_after_index_midnight.isoformat() + 'Z'

# Setup gcal
gcal.init(index_formatted, day_after_index_formatted)
from gcal import event_list
print(event_list)

#Function definitions
def strip_and_datetime(time_string):
    stripped = str(time_string)[:19]
    return dt.strptime(stripped, "%Y-%m-%dT%H:%M:%S")

##################
# Run the script #
##################
# Setup Airtable
task_name_project_id = make_dictionary_of_table()

for event in event_list:
    if event[0] in event_exclude:
        continue
    elif event[0] in task_name_project_id:
        projectid = task_name_project_id[event[0]][0]
    else:
        projectid = task_name_project_id["Uncategorized"][0]

    #Generate datetime objects
    start_time_dt = strip_and_datetime(event[1])
    end_time_dt = strip_and_datetime(event[2])

    # Convert to unix
    start_time_ts = time.mktime(start_time_dt.timetuple())
    end_time_ts = time.mktime(end_time_dt.timetuple())

    # Calculate time in hours and minutes
    hourduration = int(end_time_ts-start_time_ts) / 3600

    month = int(event[1][5:7])
    day = int(event[1][8:10])
    hour = int(event[1][11:13])

    toggl.createTimeEntry(description=event[0],
                          hourduration=hourduration,
                          projectid=projectid,
                          month=month,
                          day=day,
                          hour=hour)
