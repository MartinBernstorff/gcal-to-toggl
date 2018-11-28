from toggl.TogglPy import Toggl
from credentials import TOGGL_TOKEN
from pprint import pprint

airtable_projects = ["Morning-routine", "test2", "Family"]

toggl = Toggl()

toggl.setAPIKey(TOGGL_TOKEN)

clients = toggl.getClients()

toggl_projects = []

for client in clients:
    projects = toggl.getClientProjects(client["id"])
    if projects != None:
        for project in projects:
            toggl_projects.append(project)


for project in projects:
    if project["name"] in airtable_projects:
        airtable_projects.pop(project["name"]) # Not working yet – here, remove all projects that are already in the airtable_projects list

# Then iterate over the remaining projects and add as "name" "id" pairs to airtable

pprint(airtable_projects)
