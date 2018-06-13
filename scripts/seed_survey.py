import json
from pathlib import Path

from pymongo import MongoClient


# URL = 'mongodb+srv://tc-atlas-admin-stage:Teamculture2018@teamculture-tenant-hsfqi.mongodb.net'
URL = 'localhost:27017'


if __name__ == '__main__':
    path = Path(__file__).parent.joinpath('survey_example.json')
    with path.open() as file:
        record = json.load(file)

    client = MongoClient(URL)
    client['survey-test']['temp'].drop()
    client['survey-test']['temp'].insert(record)
