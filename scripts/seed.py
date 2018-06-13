import json
from pathlib import Path

from pymongo import MongoClient


# URL = 'mongodb+srv://tc-atlas-admin-stage:Teamculture2018@teamculture-tenant-hsfqi.mongodb.net'
URL = 'localhost:27017'


def replace_collection(dbname, collection):
    path = Path(__file__).parent.joinpath(f'{collection}.json')
    with path.open() as file:
        record = json.load(file)

    client = MongoClient(URL)
    coll = client[dbname][collection]
    coll.drop()
    coll.insert(record)


if __name__ == '__main__':
    replace_collection('survey-test', 'survey_example')
    replace_collection('survey-test', 'metrics')
