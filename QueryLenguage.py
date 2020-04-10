from enum import Enum
import json

from Structure import Project, Status, Field


class Criteria:

    def __init__(self, *args: Project):
        self.params = {"criterions": "", "projectQuery": None, "orderBy": ""}
        self.startAt = None
        self.maxResults = None
        self.fields = None
        if len(args) == 1:
            self.params["projectQuery"] = 'project = "{}"'.format(args[0].description)
        else:
            query = ""
            for val in args:
                query = query + '"{}",'.format(val.description)
            query = query[:-1]
            self.params["projectQuery"] = "project in ({})".format(query)

    def add(self, criterion):
        self.params["criterions"] = self.params["criterions"] + (" and " + criterion.__str__())
        return self

    def add_order(self, *args: Field):
        query = " ORDER BY "
        for val in args:
            query = query + '"{}", '.format(val.description)
        query = query[:-2]
        self.params["orderBy"] = query
        return self

    def page_start_at(self, index):
        self.startAt = index
        return self

    def page_limit(self, limit):
        self.maxResults = limit
        return self

    def add_response_fields(self, *args: Field):
        self.fields = list(map(lambda x: x.description, args))
        return self

    def query_build(self):
        return "{projectQuery}{criterions}{orderBy}".format(**self.params)

    def query_json(self):
        body = {'jql': self.query_build()}
        if self.startAt is not None:
            body['startAt'] = self.startAt
        if self.maxResults is not None:
            body['maxResults'] = self.maxResults
        if self.fields is not None:
            body['fields'] = self.fields
        return json.dumps(body)


class Restrictions:

    def eq(field: Field, value):
        return '{} = "{}"'.format(field.description, value)

    def not_eq(field: Field, value):
        return '{} != "{}"'.format(field.description, value)

    def is_null(field: Field):
        return '{} is null'.format(field.description)

    def is_no_null(field: Field):
        return '{} is not null'.format(field.description)

    def in_field(field: Field, *args: str):
        fieldname = field.description
        query = ""
        for val in args:
            query = query + '"{}",'.format(val)
        query = query[:-1]
        return "{} in ({})".format(fieldname, query)

    def change_status_during(status_from: set, status_to: Status, date_from:str, date_to:str):
        query = "("
        for val in status_from:
            query = query + '"{}", '.format(val.description)
        query = query[:-2] + ")"
        return 'status changed FROM {} TO "{}" DURING ("{}", "{}")'.format(query, status_to.description, date_from, date_to)

    def change_to_status_during(status_to: Status, date_from:str, date_to:str):
        return 'status changed TO "{}" DURING ("{}", "{}")'.format(status_to.description, date_from, date_to)

    def eq_enum(args: Enum):
        field_name = args.__class__.__name__
        return '{} = "{}"'.format(field_name, args.description)

    def not_eq_enum(args: Enum):
        field_name = args.__class__.__name__
        return '{} != "{}"'.format(field_name, args.description)

    def in_enum(*args: Enum):
        fieldname = args[0].__class__.__name__
        query = ""
        for val in args:
            query = query + '"{}",'.format(val.description)
        query = query[:-1]
        return "{} in ({})".format(fieldname, query)

    def add_or(*args: str):
        query = '({}'.format(args[0])
        for val in args[1:]:
            query = query + ' or {}'.format(val)
        query = query + ')'
        return query

    def add_and(*args: str):
        query = '({}'.format(args[0])
        for val in args[1:]:
            query = query + ' and {}'.format(val)
        query = query + ')'
        return query
