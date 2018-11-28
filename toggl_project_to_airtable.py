from credentials import TOGGL_TOKEN, AIRTABLE_API_KEY
from airtable_integrations import make_dictionary_of_table
from toggl_integrations import get_projects, get_project_name_id
from pprint import pprint
from airtable import Airtable

airtable = Airtable("app2VbjON28CVSlD1", "Projects", api_key=AIRTABLE_API_KEY)

airtable_projects = make_dictionary_of_table(table="Projects")

toggl_projects = get_projects()

pprint(toggl_projects)

for project in toggl_projects:
    if project["name"] not in airtable_projects:
        print("Toggl {} not found in Airtable, adding!".format(project["name"]))
        airtable.insert({"Name": project["name"],
                         "ID": project["id"]})
