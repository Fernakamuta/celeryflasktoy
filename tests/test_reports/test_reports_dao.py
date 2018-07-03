from pathlib import Path
import json
import datetime as dt

import pytest
import mongomock

from app.report.dao import DataAccessObject


@pytest.fixture
def dbname():
    return 'survey-test'


@pytest.fixture
def dao():
    client = mongomock.MongoClient()
    dao_ = DataAccessObject({'MONGO_URL': 'randomhost:42666'})
    dao_.client = client
    return dao_


class TestDao:
    def test_replace_report(self, dao, dbname):
        records_in = [
            {
                'group_id': 'g1',
                'date': dt.datetime(2017, 1, 1, 2),
                'metrics': {'m1': 10, 'm2': 10},
                'score': 10,
            },
            {
                'group_id': 'g1',
                'date': dt.datetime(2017, 1, 1, 2),
                'metrics': {'m1': 0, 'm2': 0},
                'score': 0,
            },
        ]

        group_id = 'g1'
        date = dt.datetime(2017, 1, 1, 2)
        record_expected = {
            'group_id': 'g1',
            'date': dt.datetime(2017, 1, 1, 2),
            'metrics': {'m1': 0, 'm2': 0},
            'score': 0,
        }

        # execute twice to check if it will replace
        for record_in in records_in:
            dao.replace_report(dbname, record_in)

        query = {
            'group_id': group_id,
            'date': date
        }
        cursor = dao.client[dbname].reports.find(query, {'_id': False})
        records = list(cursor)

        assert len(records) == 1
        assert record_expected == records[0]
