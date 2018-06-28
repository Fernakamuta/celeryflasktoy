import json
import datetime as dt
from pathlib import Path

import pytest


from app.services.sampler.parser import (
    _question_dts_from_scores,
    _question_dts_from_metrics,
    _merge_question_dts,
    _create_question,
    survey_from_tuples,
)
from app.services import survey2scores


@pytest.fixture
def metrics():
    path = Path(__file__).parent.joinpath('data')
    with path.joinpath('metrics_example.json').open() as file:
        metrics_ = json.load(file)
    return metrics_


@pytest.fixture
def survey():
    path = Path(__file__).parent.joinpath('data', 'survey_post_example.json')
    with path.open() as file:
        survey_ = json.load(file)
    return survey_['survey']


class TestParser:
    def test_question_dts_from_metric(self, metrics):
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

        question_dts = _question_dts_from_metrics(metrics)

        assert question_dts == question_dts_expected

    def test_question_dts_from_historic1(self):
        scores = [
            {
                'metric_id': 'm1',
                'submetric_id': 'm1s1',
                'question_id': 'm1s1q1',
                'score': -2,
                'date': dt.datetime(2017, 1, 1),
            },
            {
                'metric_id': 'm2',
                'submetric_id': 'm2s2',
                'question_id': 'm2s2q2',
                'score': 0,
                'date': dt.datetime(2017, 2, 1),
            }
        ]
        question_dts_expected = {
            'm1': {'m1s1': {'m1s1q1': dt.datetime(2017, 1, 1)}},
            'm2': {'m2s2': {'m2s2q2': dt.datetime(2017, 2, 1)}},
        }

        question_dts = _question_dts_from_scores(scores)

        assert question_dts == question_dts_expected

    def test_question_dts_from_historic2(self):
        scores = [
            {
                'metric_id': 'm1',
                'submetric_id': 'm1s1',
                'question_id': 'm1s1q1',
                'score': -2,
                'date': dt.datetime(2017, 1, 1),
            },
            {
                'metric_id': 'm1',
                'submetric_id': 'm1s1',
                'question_id': 'm1s1q1',
                'score': 0,
                'date': dt.datetime(2017, 2, 1),
            },
        ]
        question_dts_expected = {
            'm1': {'m1s1': {'m1s1q1': dt.datetime(2017, 2, 1)}},
        }

        question_dts = _question_dts_from_scores(scores)

        assert question_dts == question_dts_expected

    def test_create_question(self):
        m_id = 'm1'
        s_id = 's1'

        question_input = {
            'question_id': 'm1s1q1',
            'text': 'text-m1s1q1',
            'type': 'radio-string',
            'answers': [
                {
                    'answer_id': 'm1s1q1a1',
                    'score': -2,
                    'text': 'text-m1s1q1a1',
                    'feedback': 'positive'
                },
                {
                    'answer_id': 'm1s1q1a2',
                    'score': 0,
                    'text': 'text-m1s1q1a2',
                    'feedback': 'negative'
                }
            ],
        }

        question_expected = {
            'metric_id': 'm1',
            'submetric_id': 's1',
            'question_id': 'm1s1q1',
            'text': 'text-m1s1q1',
            'type': 'radio-string',
            'answers': [
                {
                    'answer_id': 'm1s1q1a1',
                    'score': -2,
                    'text': 'text-m1s1q1a1',
                    'feedback': 'positive'
                },
                {
                    'answer_id': 'm1s1q1a2',
                    'score': 0,
                    'text': 'text-m1s1q1a2',
                    'feedback': 'negative'
                }
            ]
        }

        question = _create_question(m_id, s_id, question_input)

        assert question == question_expected

    def test_merge_question_dts(self):
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

        question_dts = _merge_question_dts(question_dts_all, question_dts_done)

        assert question_dts == question_dts_expected


    def test_survey_from_tuples(self, metrics):
        tuples = [
            ('m1', 'm1s1', 'm1s1q1'),
            ('m2', 'm2s1', 'm2s1q2'),
        ]
        survey_expected = [
            {
                'metric_id': 'm1',
                'submetric_id': 'm1s1',
                'question_id': 'm1s1q1',
                'answers': [
                    {
                        'answer_id': 'm1s1q1a1',
                        'score': -2,
                        'text': 'text-m1s1q1a1',
                    },
                    {
                        'answer_id': 'm1s1q1a2',
                        'score': 0,
                        'text': 'text-m1s1q1a2',
                    }
                ],
                'text': 'text-m1s1q1',
                'type': 'radio-string',
            },
            {
                'metric_id': 'm2',
                'submetric_id': 'm2s1',
                'question_id': 'm2s1q2',
                'answers': [
                    {
                        'answer_id': 'm2s1q2a1',
                        'score': -2,
                        'text': 'text-m2s1q2a1',
                        'feedback': 'positive'
                    },
                    {
                        'answer_id': 'm2s1q2a2',
                        'score': 0,
                        'text': 'text-m2s1q2a2',
                        'feedback': 'positive'
                    }
                ],
                'text': 'text-m2s1q2',
                'type': 'radio-string'
            },
        ]

        survey = survey_from_tuples(metrics, tuples)

        assert survey == survey_expected


class TestParserFromPost:
    def test_survey2scores(self, survey):
        now = dt.datetime.now()
        groups = ['sciensa', 'teamculture']
        scores_expected = [
            {
                'metric_id': 'ambassadorship',
                'submetric_id': 'promotor',
                'group_ids': ['sciensa', 'teamculture'],
                'question_id': 'promotor5',
                'answer_id': None,
                'score': None,
                'feedback': None,
                'date': now
            },
            {
                'metric_id': 'alignment',
                'submetric_id': 'vision',
                'group_ids': ['sciensa', 'teamculture'],
                'question_id': 'vision1',
                'answer_id': "visionAnswer1e",
                'score': 2,
                'feedback': None,
                'date': now
            },
            {
                'metric_id': 'feedback',
                'submetric_id': 'quality',
                'group_ids': ['sciensa', 'teamculture'],
                'question_id': 'quality4',
                'answer_id': "trust_answer4k",
                'score': 2,
                'feedback': {
                    "text": "Porque a empresa é demais!",
                    "is_annonymous": False
                },
                'date': now
            }
        ]

        scores = survey2scores(survey, groups, now)

        assert scores == scores_expected
