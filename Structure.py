from enum import Enum


class Project(Enum):
    OAS = "OAS",
    WOLFF = "WOLFF",
    APIO = "CFA API Oracle",
    MIX = "MIX",
    NOTO = "NOTO"

    def __init__(self, description):
        self.description = description


class Labels(Enum):
    SP = "SP",
    LT_OK = "LT_OK",

    def __init__(self, description):
        self.description = description


class Status(Enum):
    BACKLOG = "Backlog",
    STORY_SELECTED = "Story Selected",
    STORY_WAITING_REVIEW = "Story waiting review",
    STORY_PROGRESS = "Story in progress",
    DONE = "Done"

    def __init__(self, description):
        self.description = description


class Field(Enum):
    LABELS = "labels",
    ASSIGNEE = "assignee",
    PRIORITY = "priority",
    PROJECT = "project",
    KEY = "key",
    ITEMS = "items",
    STATUS = "status",
    ISSUETYPE = "issuetype",
    REPORTER = "reporter",
    SUMMARY = "summary"

    def __init__(self, description):
        self.description = description

class User(Enum):
    JAVI = "javier.robles",
    JULI = "julian.colaiacovo",
    JOACO = "joaquin.nacht",
    FRAN = "franco.cerquetti",
    GUIDO = "guido.deluca"

    def __init__(self, description):
        self.description = description


class Operator(Enum):
    AND = "AND",
    OR = "OR",
    IN = "IN",
    NOT = "NOT",
    NOT_IN = "NOT IN",
    IS = "IS"

    def __init__(self, description):
        self.description = description
