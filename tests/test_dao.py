import json
from pathlib import Path

import pytest
import mongomock

from app.dao import parse_i18n, DataAccessObject


@pytest.fixture
def dbname():
    return 'survey-test'


@pytest.fixture
def dao(dbname):
    path = Path(__file__).parent.joinpath('data', 'metrics_example.json')
    with path.open() as file:
        metrics = json.load(file)

    client = mongomock.MongoClient()
    client[dbname].metrics.insert(metrics)

    dao_ = DataAccessObject()
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

        assert record == record_expected

    def test_find_metrics(self, dao, dbname):

        records = dao.find_metrics(dbname, 'pt-br')

        assert len(records) == 3
