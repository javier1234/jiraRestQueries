import unittest
from QueryLenguage import Criteria, Restrictions
from Structure import Project, Labels, Status, Field


class TestSum(unittest.TestCase):

    def test_criteria_project(self):
        c1p = Criteria(Project.OAS)
        c_more_pro = Criteria(Project.OAS, Project.WOLFF)

        self.assertEqual(c1p.query_build(), 'project = "OAS"')
        self.assertEqual(c_more_pro.query_build(), 'project in ("OAS","WOLFF")')

    def test_criteria_add_sql(self):
        c = Criteria(Project.OAS)
        c.add('field = "value"')

        self.assertEqual('project = "OAS" and field = "value"', c.query_build())

    def test_restriction(self):
        c = Criteria(Project.OAS)
        c.add(Restrictions.eq(Field.ASSIGNEE, "value"))

        self.assertEqual('project = "OAS" and assignee = "value"', c.query_build())

    def test_restrictions(self):
        c = Criteria(Project.OAS)
        c.add(Restrictions.eq(Field.ASSIGNEE, "value"))
        c.add(Restrictions.eq(Field.KEY, "value"))

        self.assertEqual('project = "OAS" and assignee = "value" and key = "value"', c.query_build())

    def test_restriction_in_enum(self):
        c = Criteria(Project.OAS)
        c.add(Restrictions.in_enum(Labels.LT_OK))

        self.assertEqual('project = "OAS" and Labels in ("LT_OK")', c.query_build())

        c = Criteria(Project.OAS)
        c.add(Restrictions.in_enum(Labels.LT_OK, Labels.SP))

        self.assertEqual('project = "OAS" and Labels in ("LT_OK","SP")', c.query_build())

    def test_restriction_eq_enum(self):
        c = Criteria(Project.OAS)
        c.add(Restrictions.eq_enum(Labels.LT_OK))

        self.assertEqual('project = "OAS" and Labels = "LT_OK"', c.query_build())

    def test_or(self):
        c = Criteria(Project.OAS)
        or_query = Restrictions.add_or(Restrictions.eq_enum(Labels.LT_OK), Restrictions.eq(Field.ASSIGNEE, "valor"))
        c.add(or_query)

        self.assertEqual('project = "OAS" and (Labels = "LT_OK" or assignee = "valor")', c.query_build())

    def test_and(self):
        c = Criteria(Project.OAS)
        c.add(Restrictions.add_and(Restrictions.eq_enum(Labels.LT_OK), Restrictions.eq(Field.ASSIGNEE, "valor")))

        self.assertEqual('project = "OAS" and (Labels = "LT_OK" and assignee = "valor")', c.query_build())

    def test_is_null(self):
        c = Criteria(Project.OAS)
        c.add(Restrictions.is_null(Field.ASSIGNEE))

        self.assertEqual('project = "OAS" and assignee is null', c.query_build())

    def test_during(self):
        c = Criteria(Project.OAS)
        c.add(
            Restrictions.change_status_during([Status.STORY_PROGRESS, Status.STORY_SELECTED], Status.HIST_ANALISIS_FUN,
                                              '2020/01/01', '2020/02/02'))

        self.assertEqual('project = "OAS" and status changed FROM ("Story in progress", "Story Selected") TO '
                         '"HISTORIA EN ANALISIS FUNCIONAL" DURING ("2020/01/01", "2020/02/02")', c.query_build())

    def test_order(self):
        c = Criteria(Project.OAS)
        c.add_order(Field.ASSIGNEE, Field.KEY)

        self.assertEqual('project = "OAS" ORDER BY "assignee", "key"', c.query_build())

    def test_json(self):
        c = Criteria(Project.OAS)
        c.page_limit(10)
        c.page_start_at(5)

        self.assertEqual('{"jql": "project = \\"OAS\\"", "startAt": 5, "maxResults": 10}', c.query_json().__str__())

    def test_fields(self):
        c = Criteria(Project.OAS)
        c.add_response_fields(Field.KEY, Field.ASSIGNEE)

        self.assertEqual('{"jql": "project = \\"OAS\\"", "fields": ["key", "assignee"]}', c.query_json().__str__())



if __name__ == '__main__':
    unittest.main()
