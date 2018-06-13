from pymongo import MongoClient


def stringfy_id(record):
    record_new = {
        **record,
        '_id': str(record['_id'])
    }
    return record_new


class DataAccessObject:
    def __init__(self):
        self.client = None

    def init_app(self, config):
        self.client = MongoClient(config['MONGO_URL'])

    def find_temp(self):
        cursor = self.client['master']['temp'].find()
        record, *_ = list(cursor)
        return stringfy_id(record)
