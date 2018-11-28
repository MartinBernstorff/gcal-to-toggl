from airtable import Airtable
from credentials import AIRTABLE_API_KEY
from pprint import pprint

def make_dictionary_of_table(baseKey="app2VbjON28CVSlD1", table="Tasks", view='Grid view', key_column="Name", value_column="ID"):

    airtable = Airtable(baseKey, table, api_key=AIRTABLE_API_KEY)

    dict = {}

    for page in airtable.get_iter(view=view, sort=key_column):
        for record in page:
            dict[record['fields'][key_column]] = record['fields'][value_column]

    return dict

def make_list_of_table(baseKey="app2VbjON28CVSlD1", table="Tasks", view='Grid view', key_column="Name", value_column="ID"):

    airtable = Airtable(baseKey, table, api_key=AIRTABLE_API_KEY)

    list = []

    for page in airtable.get_iter(view=view, sort=key_column):
        for record in page:
            list.append((record['fields'][key_column], record['fields'][value_column]))

    return list
