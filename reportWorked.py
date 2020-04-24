import os
import webbrowser
import datetime

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

today = datetime.date.today()
last_monday = today - datetime.timedelta(days=today.weekday())
coming_friday = last_monday + datetime.timedelta(days=4)
toDate = last_monday.strftime("%Y/%m/%d")
fromDate = coming_friday.strftime("%Y/%m/%d")

# que hicimos de lo que estaba en el sprint
criteria_do_worked_sprint = Criteria(*ALL_PROJECTS_MY_TEAM)\
    .add(Restrictions.eq_enum(Labels.SP))\
    .add(Restrictions.change_to_status_during(Status.STORY_WAITING_REVIEW, toDate, fromDate))\
    .add(storyWorkByMyTeam)\
    .add_order(Field.ASSIGNEE, Field.PRIORITY, Field.PROJECT, Field.KEY)\
    .add_response_fields(Field.KEY, Field.ASSIGNEE, Field.ITEMS, Field.STATUS, Field.PRIORITY, Field.ISSUETYPE, Field.REPORTER, Field.SUMMARY)

# que no llegamo a terminar
criteria_not_worked_sprint = Criteria(*ALL_PROJECTS_MY_TEAM)\
    .add(Restrictions.eq_enum(Labels.SP))\
    .add(Restrictions.in_enum(Status.BACKLOG, Status.STORY_SELECTED, Status.STORY_PROGRESS))\
    .add(storyWorkByMyTeam)\
    .add_order(Field.ASSIGNEE, Field.PRIORITY, Field.PROJECT, Field.KEY)\
    .add_response_fields(Field.KEY, Field.ASSIGNEE, Field.ITEMS, Field.STATUS, Field.PRIORITY, Field.ISSUETYPE, Field.REPORTER, Field.SUMMARY)


# que tomamos por fuera
criteria_do_worked_out_sprint = Criteria(*ALL_PROJECTS_MY_TEAM)\
    .add(Restrictions.add_or(Restrictions.not_eq_enum(Labels.SP), Restrictions.is_null(Field.LABELS)))\
    .add(Restrictions.change_to_status_during(Status.STORY_PROGRESS, toDate, fromDate))\
    .add(storyWorkByMyTeam)\
    .add_order(Field.ASSIGNEE, Field.PRIORITY, Field.PROJECT, Field.KEY)\
    .add_response_fields(Field.KEY, Field.ASSIGNEE, Field.ITEMS, Field.STATUS, Field.PRIORITY, Field.ISSUETYPE, Field.REPORTER, Field.SUMMARY)

# print(c.query_json())

reportJsonWorkedInSprint = JiraConnector().search(criteria_do_worked_sprint)
jirasByDevsWorkedSprint = {}
for issue in reportJsonWorkedInSprint["issues"]:
    row = JiraData(issue)
    if row.user not in jirasByDevsWorkedSprint.keys():
        jirasByDevsWorkedSprint[row.user] = list()
    jirasByDevsWorkedSprint[row.user].append(row)

reportJsonNotWorkedSprint = JiraConnector().search(criteria_not_worked_sprint)
jirasByDevsNotWorkedSprint = {}
for issue in reportJsonNotWorkedSprint["issues"]:
    row = JiraData(issue)
    if row.user not in jirasByDevsNotWorkedSprint.keys():
        jirasByDevsNotWorkedSprint[row.user] = list()
    jirasByDevsNotWorkedSprint[row.user].append(row)

reportJsonWorkedOutSprint = JiraConnector().search(criteria_do_worked_out_sprint)
jirasByDevsWorkedOutSprint = {}
for issue in reportJsonWorkedOutSprint["issues"]:
    row = JiraData(issue)
    if row.user not in jirasByDevsWorkedOutSprint.keys():
        jirasByDevsWorkedOutSprint[row.user] = list()
    jirasByDevsWorkedOutSprint[row.user].append(row)


html = HtmlFile()
html.title("Resultado de la semana {} al {}".format(last_monday.strftime("%d-%m"), coming_friday.strftime("%d-%m")))

html.paragraphTitle("Tareas agendadas en la semana y finalizadas")
for user, data in jirasByDevsWorkedSprint.items():
    html.seccionTitle(user)
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

html.add_br(3)

html.paragraphTitle("Tareas agendadas pero no finalizadas")
for user, data in jirasByDevsNotWorkedSprint.items():
    html.seccionTitle(user)
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

html.add_br(3)

html.paragraphTitle("Tareas trabajadas por fuera de la agenda")
for user, data in jirasByDevsWorkedOutSprint.items():
    html.seccionTitle(user)
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
f = open("worked.html", "w")
f.write(html.get_html())
f.close()
webbrowser.open('file://' + os.path.realpath(f.name))