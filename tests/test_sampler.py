import pytest
import json
import datetime as dt
from pathlib import Path

from app.services.sampler import Sampler


@pytest.fixture
def sampler():
    return Sampler()


@pytest.fixture
def metrics():
    path = Path(__file__).parent.joinpath('data')
    with path.joinpath('metrics_example.json').open() as file:
        metrics = json.load(file)
    return metrics


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
    def test_select_questions(self, sampler, questions, n, tuples_expected):
        tuples = sampler._select_questions(questions, n)
        assert set(tuples) == set(tuples_expected)

    def test_question_dts_from_metric(self, sampler, metrics):
        old = dt.datetime(dt.MINYEAR, 1, 1)
        question_dts_expected = {
            'm1': {
                'm1s1': {
                    'm1s1q1': old,
                    'm1s1q2': old,
                },
                'm1s2': {
                    'm1s2q1': old,
                    'm1s2q2': old,
                }
            },
            'm2': {
                'm2s1': {
                    'm2s1q1': old,
                    'm2s1q2': old,
                },
                'm2s2': {
                    'm2s2q1': old,
                    'm2s2q2': old,
                }
            },
        }

        question_dts = sampler._question_dts_from_metrics(metrics)

        assert question_dts == question_dts_expected

    def test_question_dts_from_historic(self, sampler):
        historic = {
          "email": "test@test.com",
          "scores": [
            {
              "metric_id": "m1",
              "submetric_id": "m1s1",
              "question_id": "m1s1q1",
              "score": -2,
              "date": dt.datetime(2017, 1, 1),
            },
            {
              "metric_id": "m2",
              "submetric_id": "m2s2",
              "question_id": "m2s2q2",
              "score": 0,
              "date": dt.datetime(2017, 2, 1),
            }
          ]
        }
        question_dts_expected = {
            'm1': {'m1s1': {'m1s1q1': dt.datetime(2017, 1, 1)}},
            'm2': {'m2s2': {'m2s2q2': dt.datetime(2017, 2, 1)}},
        }

        question_dts = sampler._question_dts_from_historic(historic)

        assert question_dts == question_dts_expected

    def test_merge_question_dts(self, sampler):
        old = dt.datetime(dt.MINYEAR, 1, 1)
        question_dts_all = {
            'm1': {
                's1': {
                    'q1': old,
                    'q2': old,
                }
            },
            'm2': {
                's1': {
                    'q1': old,
                    'q2': old,
                }
            },
        }
        question_dts_done = {
            'm1': {'s1': {'q1': dt.datetime(2017, 1, 1)}},
            'm2': {'s1': {'q2': dt.datetime(2017, 1, 1)}},
        }
        question_dts_expected = {
            'm1': {
                's1': {
                    'q1': dt.datetime(2017, 1, 1),
                    'q2': old,
                }
            },
            'm2': {
                's1': {
                    'q1': old,
                    'q2': dt.datetime(2017, 1, 1),
                }
            },
        }

        question_dts = sampler._merge_question_dts(question_dts_all, question_dts_done)

        assert question_dts == question_dts_expected

    def test_survey_from_tuples(self, sampler, metrics):
        tuples = [
            ('m1', 'm1s1', 'm1s1q1'),
            ('m2', 'm2s1', 'm2s1q2'),
        ]
        survey_expected = [
            {
                "metric_id": "m1",
                "submetric_id": "m1s1",
                "question_id": "m1s1q1",
                "answers": [
                    {
                        "answer_id": "m1s1q1a1",
                        "score": -2,
                        "text": "text-m1s1q1a1"
                    },
                    {
                        "answer_id": "m1s1q1a2",
                        "score": 0,
                        "text": "text-m1s1q1a2"
                    }
                ],
                "text": "text-m1s1q1",
                "type": "radio-string",
            },
            {
                "metric_id": "m2",
                "submetric_id": "m2s1",
                "question_id": "m2s1q2",
                "answers": [
                    {
                        "answer_id": "m2s1q2a1",
                        "score": -2,
                        "text": "text-m2s1q2a1"
                    },
                    {
                        "answer_id": "m2s1q2a2",
                        "score": 0,
                        "text": "text-m2s1q2a2"
                    }
                ],
                "text": "text-m2s1q2",
                "type": "radio-string"
            },
        ]

        survey = sampler._survey_from_tuples(metrics, tuples)

        assert survey == survey_expected
