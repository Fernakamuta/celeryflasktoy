import datetime as dt

from app.report.stats import generate_report


class TestStats:
    def test_generate_report(self):
        now = dt.datetime.now()
        metric_ids = ['m1', 'm2']
        group_id = 'g1'
        scsores_in = [
            {
                'metric_id': 'm1',
                'submetric_id': 's1',
                'question_id': 'q1',
                'score': +2,
                'date': now,
                'group_ids': ['g1', 'g2'],
                'email': 'test@test.com',
            },
            {
                'metric_id': 'm1',
                'submetric_id': 's1',
                'question_id': 'q1',
                'score': -2,
                'date': now,
                'group_ids': ['g1', 'g2'],
                'email': 'test@test.com',
            },
        ]
        record_expected = {
            'group_id': 'g1',
            'metrics': [
                {'metric_id': 'm1', 'score': 0},
                {'metric_id': 'm2', 'score': None},
            ],
            'score': 0,
        }

        record = generate_report(group_id, metric_ids, scsores_in)
        assert 'date' in record
        del record['date']
        assert record_expected == record
