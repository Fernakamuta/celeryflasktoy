import datetime as dt

import pytest

from app.report.stats.core import (
    _compute_sole_scores,
    _compute_group_scores,
    _compute_overall,
    compute_scores,
)


class TestCore:
    def test_compute_sole_score(self):
        record_in = {
            'm1': {
                's1': {
                    'q1': [(-2, dt.datetime(2017, 1, 1)), (2, dt.datetime(2017, 2, 1))],
                    'q2': [(-2, dt.datetime(2017, 1, 2)), (2, dt.datetime(2017, 2, 2))],
                },
                's2': {
                    'q1': [(-2, dt.datetime(2017, 1, 1)), (2, dt.datetime(2017, 2, 1))],
                    'q2': [(-2, dt.datetime(2017, 1, 2)), (2, dt.datetime(2017, 2, 2))],
                },
            },
            'm2': {
                's1': {
                    'q1': [(-2, dt.datetime(2017, 1, 1)), (0, dt.datetime(2017, 2, 1))],
                    'q2': [(-2, dt.datetime(2017, 1, 2)), (0, dt.datetime(2017, 2, 2))],
                },
                's2': {
                    'q1': [(None, dt.datetime(2017, 1, 1)), (-1, dt.datetime(2017, 2, 1))],
                    'q2': [(None, dt.datetime(2017, 1, 2)), (None, dt.datetime(2017, 2, 2))],
                },
            },
        }
        record_expected = {'m1': 0, 'm2': -1}

        record = _compute_sole_scores(record_in)

        assert record_expected == record

    def test_compute_group_score(self):
        metric_ids = ['m1', 'm2', 'm3']
        records_in = [
            {'m1': +2, 'm2': -1},
            {'m1': -2, 'm2': +1},
        ]
        record_expected = {
            'm1': 0,
            'm2': 0,
            'm3': None
        }

        record = _compute_group_scores(metric_ids, records_in)

        assert record_expected == record

    tuples = [
        ({'m1': -2,'m2': +2,'m3': None}, 0),
        ({'m1': None, 'm2': None}, None),
    ]

    @pytest.mark.parametrize('record_in, overall_expected', tuples)
    def test_compute_overall(self, record_in, overall_expected):

        overall = _compute_overall(record_in)

        assert overall_expected == overall

    def test_compute_scores(self):
        metric_ids = ['m1', 'm2']
        records = [
            {
                'm1': {'s1': {'q1': [(-2, dt.datetime(2017, 1, 1)), (2, dt.datetime(2017, 2, 1))]}},
                'm2': {'s1': {'q1': [(-2, dt.datetime(2017, 1, 1)), (2, dt.datetime(2017, 2, 1))]}},
            },
            {
                'm1': {'s1': {'q1': [(None, dt.datetime(2017, 1, 1)), (0, dt.datetime(2017, 2, 1))]}},
                'm2': {'s1': {'q1': [(None, dt.datetime(2017, 1, 1)), (None, dt.datetime(2017, 2, 1))]}},
            },
        ]
        overall_expected = 0
        record_expected = {'m1': 0, 'm2': 0}

        overall, record = compute_scores(metric_ids, records)

        assert overall_expected == overall
        assert record_expected == record
