# Date and time improts
import datetime
import time
from datetime import datetime as dt
import sys

# Integration imports
from credentials import TOGGL_TOKEN, AIRTABLE_API_KEY
from toggl.TogglPy import Toggl
from airtable import Airtable
from airtable_integrations import *
import gcal

#Utilities
import re
from pprint import pprint
from task_dicts import event_exclude
import urllib

toggl = Toggl()

toggl.setAPIKey(TOGGL_TOKEN)

offset = int(sys.argv[1])

#Generate today-string
index = dt.today() + datetime.timedelta(offset)
index_midnight = index.replace(hour=0, minute=1)
index_formatted = index_midnight.isoformat() + 'Z'
index_str = dt.strftime(index,'%Y-%m-%d')

day_after_index = index + datetime.timedelta(1)
day_after_index_midnight = day_after_index.replace(hour=0, minute=1)
day_after_index_formatted = day_after_index_midnight.isoformat() + 'Z'

####################################################
# Check if entries already exist in Toggl for date #
####################################################
start_date_encoded = urllib.parse.quote(index_formatted)
end_date_encoded = urllib.parse.quote(day_after_index_formatted)

entries_on_day = toggl.request("https://www.toggl.com/api/v8/time_entries" + "?start_date=" + start_date_encoded + "&end_date=" + end_date_encoded)

assert entries_on_day == []

##############
# Setup gcal #
##############
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

task_list = make_list_of_table()

regex_task_list = []

#
for task in task_list:
    if task[0][-1:] == "*" and task[0][0] == "*":
        regex_task_list.append(task)

pprint("Regex_task_list: {}".format(regex_task_list))

for event in event_list:
    projectid = None

    print("Processing event {}".format(event[0]))
    pprint(event)
    if event[0] in event_exclude:
        continue
    elif event[0] in task_name_project_id: # If event is an exact match
        projectid = task_name_project_id[event[0]][0]
    else: # If not an exact match
        for task in regex_task_list: # Do regex matching on all Airtable tasks ending in "*"
            if re.match(".*{}.*".format(task[0][1:-1]), event[0]) != None:
                projectid = task[1][0]
                print("Task matches regex!\nProject_id: {}".format(projectid))

    if projectid is None:
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

    data = {"time_entry":
            {
                "description": event[0],
                "start": event[1],
                "duration": int(hourduration * 3600),
                "pid": projectid,
                "created_with": "gcal-to-toggl"
            }}

    pprint(data)

    response = toggl.postRequest("https://www.toggl.com/api/v8/time_entries",
                                  parameters=data)

    print(response)
