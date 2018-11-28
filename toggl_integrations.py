from credentials import TOGGL_TOKEN
from toggl.TogglPy import Toggl

def get_projects():
    """Since the current project function in PyToggl doesn't work, I made my own
    hacky version. Gets all projects assigned to a client and returns it as a
    list"""

    toggl = Toggl()

    toggl.setAPIKey(TOGGL_TOKEN)

    clients = toggl.getClients()

    toggl_projects = []

    for client in clients:
        projects = toggl.getClientProjects(client["id"])
        if projects != None:
            for project in projects:
                toggl_projects.append(project)

    return toggl_projects

def get_project_name_id():
    """Returns a dictionary of
    key: project-name (str)
    val: project-id (int)"""

    toggl_projects = get_projects()

    dict = {}

    for project in toggl_projects:
        name = project["name"]
        id = project["id"]

        dict.update({name: id})

    return dict
