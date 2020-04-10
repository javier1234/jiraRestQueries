import os
import webbrowser
from datetime import date, datetime

from QueryLenguage import Criteria, Restrictions
from Structure import Project, Status, Field, Labels, User
from HtlmBuilder import HtmlFile, Table, Tr
from jiraRest import JiraConnector, JiraData

ALL_PROJECTS_MY_TEAM = [Project.OAS, Project.WOLFF, Project.NOTO, Project.MIX, Project.APIO]
ALL_DEV_TEAM = [User.FRAN.description, User.GUIDO.description, User.JAVI.description, User.JOACO.description, User.JULI.description]

storySprintSelected = Restrictions.add_and(Restrictions.eq_enum(Labels.SP), Restrictions.in_enum(Status.BACKLOG, Status.STORY_SELECTED, Status.STORY_PROGRESS))
storyInProgress = Restrictions.in_enum(Status.STORY_PROGRESS)
storyByWork = Restrictions.add_or(storySprintSelected, storyInProgress)
storyWorkByMyTeam = Restrictions.in_field(Field.ASSIGNEE, *ALL_DEV_TEAM)

# historias para tomar esta semana, tageadas con el label de SP o en progreso
c = Criteria(*ALL_PROJECTS_MY_TEAM)\
    .add(storyByWork)\
    .add(storyWorkByMyTeam)\
    .add_order(Field.ASSIGNEE, Field.PRIORITY, Field.PROJECT, Field.KEY)\
    .add_response_fields(Field.KEY, Field.ASSIGNEE, Field.ITEMS, Field.STATUS, Field.PRIORITY, Field.ISSUETYPE, Field.REPORTER, Field.SUMMARY)

# print(c.query_json())

reportJson = JiraConnector().search(c)
jirasByDevs = {}
for issue in reportJson["issues"]:
    row = JiraData(issue)
    if row.user not in jirasByDevs.keys():
        jirasByDevs[row.user] = list()
    jirasByDevs[row.user].append(row)

html = HtmlFile()
now = datetime.now()
date_time = now.strftime("%d/%m/%Y")
html.title("Tareas asignadas semana {}".format(date_time))

for user, data in jirasByDevs.items():
    html.paragraphTitle(user)
    table = Table()
    table.add_th("Jira")
    table.add_th("Tarea", 400)
    table.add_th("Responsable", 150)
    table.add_th("Estado", 200)
    table.add_th("Prioridad")

    for row in data:
        tr = Tr()
        tr.add_td(row.key)
        tr.add_td(row.summary)
        tr.add_td(row.reporter)
        tr.add_td(row.status)
        tr.add_td(row.priority)
        table.add_tr(tr)
    html.add_table(table)

#print(html.get_html())
f = open("sprint.html", "w")
f.write(html.get_html())
f.close()
webbrowser.open('file://' + os.path.realpath(f.name))