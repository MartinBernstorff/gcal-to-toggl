from airtable import Airtable
from credentials import AIRTABLE_API_KEY
from pprint import pprint

def make_dictionary_of_base(baseKey="app2VbjON28CVSlD1", table="Tasks", view='Grid view', sort="Name"):

    airtable = Airtable(baseKey, table, api_key=AIRTABLE_API_KEY)

    task_name_project_id = {}

    for page in airtable.get_iter(view=view, sort=sort):
        for record in page:
            task_name_project_id[record['fields']['Name']] = record['fields']['ID'][0]

    return task_name_project_id
