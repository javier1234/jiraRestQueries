import requests
import json

# coding=utf-8

from QueryLenguage import Criteria
from requests.auth import HTTPBasicAuth

USER = "XXXXXX"
PASS_WORD = "XXXXXX"

JIRA_ENDPOINT = "XXXXXX"
JIRA_SEARCH_LIST = "/search"
JIRA_SEARCH_ISSUE = "/issue/{}?expand=changelog&fields=items"

class JiraData:
    def __init__(self, issue):
        self.key = '<a href="https://jira.despegar.com/browse/{}">{}</a>'.format(issue["key"],issue["key"])
        self.user = issue["fields"]["assignee"]["displayName"]
        self.status = issue["fields"]["status"]["name"]
        self.priority = issue["fields"]["priority"]["name"]
        self.itype = issue["fields"]["issuetype"]["description"]
        self.reporter = issue["fields"]["reporter"]["displayName"]
        self.summary = issue["fields"]["summary"]

class JiraConnector:
    def __init__(self):
        pass

    def search(self, criteria: Criteria):
        res = requests.post(JIRA_ENDPOINT + JIRA_SEARCH_LIST,
                            data=criteria.query_json(),
                            headers={"Content-Type": "application/json"},
                            auth=HTTPBasicAuth(USER, PASS_WORD))
        resJson = json.loads(res.content.decode("utf8"))
        print(resJson)
        return resJson

    def get(self, jiraKey: str):
        res = requests.get(JIRA_ENDPOINT + JIRA_SEARCH_ISSUE.format(jiraKey),
                            headers={"Content-Type": "application/json"},
                            auth=HTTPBasicAuth(USER, PASS_WORD))
        resJson = json.loads(res.content.decode("utf8"))
        print(resJson)
        return resJson


#c = Criteria(Project.OAS).page_start_at(0).page_limit(10)
#JiraConnector().search(c)

#JiraConnector().get("OAS-3434")