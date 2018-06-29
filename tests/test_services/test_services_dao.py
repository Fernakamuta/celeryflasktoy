import json
import datetime as dt
from pathlib import Path
from copy import deepcopy

import pytest
import mongomock


from app.survey.dao import parse_i18n, DataAccessObject


@pytest.fixture
def dbname():
    return 'survey-test'


@pytest.fixture
def dao(dbname):
    path = Path(__file__).parents[1].joinpath('data', 'metrics_example.json')
    with path.open() as file:
        metrics = json.load(file)

    client = mongomock.MongoClient()
    client[dbname].metrics.insert(metrics)

    dao_ = DataAccessObject({'MONGO_URL': 'randomhost:42666'})
    dao_.client = client
    return dao_


class TestDao:
    def test_parser_i18n(self):
        lang_in = 'en-us'
        record_in = {
            'foo': {
                'en-us': 'johnny rocket',
                'pt-br': 'joão foguete',
            },
            'bar': [
                {
                    'bar1': {
                        'en-us': 'johnny rocket',
                        'pt-br': 'joão foguete',
                    }
                }
            ],
            'foobar': {
                'pt-br': 'joão foguete',
            },
        }
        record_expected = {
            'foo': 'johnny rocket',
            'bar': [
                {
                    'bar1': 'johnny rocket',
                }
            ],
            'foobar': 'joão foguete',
        }

        record = parse_i18n(record_in, lang_in)

        assert record_expected ==  record

    def test_find_metrics(self, dao, dbname):

        records = dao.find_metrics(dbname, 'pt-br')

        assert len(records) == 2

    def test_find_scores(self, dao, dbname):
        email_in = 'test@test.com'
        scores_in = [
            {
                'metric_id': 'm1',
                'submetric_id': 'sm1',
                'question_id': 'q1',
                'score': -2,
                'date': dt.datetime(2017, 1, 1),
                'email': email_in,
            },
            {
                'metric_id': 'm2',
                'submetric_id': 'sm2',
                'question_id': 'q2',
                'score': 2,
                'date': dt.datetime(2017, 1, 1),
                'email': email_in,
            },
        ]
        dao.client[dbname].historics.insert_many(deepcopy(scores_in))

        records = dao.find_scores(dbname, email_in)

        assert records == scores_in

    def test_insert_scores(self, dao, dbname):
        email_in = 'test@test.com'
        scores_in = [
            {
                'metric_id': 'm1',
                'submetric_id': 'sm1',
                'question_id': 'q1',
                'score': -2,
                'date': dt.datetime(2017, 1, 1),
                'email': email_in,
            },
            {
                'metric_id': 'm2',
                'submetric_id': 'sm2',
                'question_id': 'q2',
                'score': 2,
                'date': dt.datetime(2017, 1, 1),
                'email': email_in,
            },
        ]

        dao.insert_scores(dbname, deepcopy(scores_in))

        cursor = dao.client[dbname].historics.find({'email': email_in}, {'_id': False})
        scores = list(cursor)

        assert scores == scores_in
