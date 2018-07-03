import pytest
import datetime as dt

from app.survey.sampler.core import select_questions


class TestSampler:
    params = [
        (
            {
                'm1': {'s1': {'q1': dt.datetime(2017, 1, 1)}},
                'm2': {'s1': {'q1': dt.datetime(2017, 2, 1)}},
                'm3': {'s1': {'q1': dt.datetime(2017, 3, 1)}},
                'm4': {'s1': {'q1': dt.datetime(2017, 4, 1)}},
            },
            2,
            [('m1', 's1', 'q1'), ('m2', 's1', 'q1')]

        ),
        (
            {
                'm1': {
                    's1': {'q1': dt.datetime(2017, 4, 1)},
                    's2': {'q1': dt.datetime(2017, 3, 1)}
                },
                'm2': {
                    's1': {'q1': dt.datetime(2017, 2, 1)},
                    's2': {'q1': dt.datetime(2017, 1, 1)}
                },
            },
            1,
            [('m2', 's2', 'q1')]

        ),
        (
            {
                'm1': {
                    's1': {
                        'q1': dt.datetime(2017, 4, 1),
                        'q2': dt.datetime(2017, 3, 1),
                        'q3': dt.datetime(2017, 2, 1),
                        'q4': dt.datetime(2017, 1, 1),
                    },
                },
            },
            1,
            [('m1', 's1', 'q4')]

        ),
        (
            {
                'm1': {
                    's1': {
                        'q1': dt.datetime(2017, 3, 1),
                        'q2': dt.datetime(2017, 1, 1),
                        'q3': dt.datetime(2017, 1, 1),
                    },
                },
                'm2': {'s1': {'q1': dt.datetime(2017, 2, 1)}},
            },
            1,
            [('m2', 's1', 'q1')]

        ),
    ]

    @pytest.mark.parametrize('questions, n, tuples_expected', params)
    def test_select_questions(self, questions, n, tuples_expected):
        tuples = select_questions(questions, n)
        assert set(tuples) == set(tuples_expected)
