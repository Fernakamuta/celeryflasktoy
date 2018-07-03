import datetime as dt

from app.report.stats.parser import _to_record, to_report


class TestParsers:
    def test_to_record(self):
        historic_in =  [
            {
                'group_id': 'g1',
                'metric_id': 'm1',
                'submetric_id': 's1',
                'question_id': 'q1',
                'score': -2,
                'date': dt.datetime(2017, 1, 1),
                'email': 'user1@test.com',
            },
            {
                'group_id': 'g1',
                'metric_id': 'm1',
                'submetric_id': 's1',
                'question_id': 'q1',
                'score': 2,
                'date': dt.datetime(2017, 1, 2),
                'email': 'user1@test.com',
            },
            {
                'group_id': 'g1',
                'metric_id': 'm2',
                'submetric_id': 's1',
                'question_id': 'q1',
                'score': 2,
                'date': dt.datetime(2017, 1, 3),
                'email': 'user1@test.com',
            },
        ]

        record_expected = {
            'm1': {'s1': {'q1': [(-2, dt.datetime(2017, 1, 1)), (2, dt.datetime(2017, 1, 2))]}},
            'm2': {'s1': {'q1': [(2, dt.datetime(2017, 1, 3))]}},
        }

        record = _to_record(historic_in)

        assert record_expected == record

    def test_to_report(self):
        group_id = 'g1'
        metric_ids = ['m1', 'm2', 'm3']
        overall = 0
        scores_m = {
            'm1': -2,
            'm2': 2,
        }

        report_expected = {
            'group_id': 'g1',
            'metrics': [
                {'metric_id': 'm1', 'score': -2},
                {'metric_id': 'm2', 'score': 2},
                {'metric_id': 'm3', 'score': None},
            ],
            'score': 0,
        }

        report = to_report(group_id, metric_ids, overall, scores_m)

        assert 'date' in report
        del report['date']
        assert report == report_expected
