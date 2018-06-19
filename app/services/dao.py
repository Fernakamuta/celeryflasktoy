from pymongo import MongoClient

from .temp import filtered_metrics


def parse_i18n(record, lang):
    default = 'pt-br'
    if isinstance(record, list):
        return [parse_i18n(each, lang) for each in record]
    if isinstance(record, dict):
        if not {lang, default} & set(record):
            return {key: parse_i18n(value, lang) for key, value in record.items()}
        return record.get(lang, record[default])
    return record


def stringfy_id(record):
    record_new = {
        **record,
        '_id': str(record['_id'])
    }
    return record_new


class DataAccessObject:
    def __init__(self, config):
        self.client = MongoClient(config['MONGO_URL'])

    def find_metrics(self, dbname, lang):
        cursor = self.client[dbname].metrics.find({}, {'_id': False})

        # temporary filter
        records = filtered_metrics(list(cursor))

        return parse_i18n(records, lang)

    def find_historic(self, dbname, email):
        query = {
            'email': email
        }
        proj = {
            '_id': False
        }
        record = self.client[dbname].historics.find_one(query, proj)
        if record:
            return record
        return {'email': email, 'scores': []}

    def update_historic(self, dbname, email, scores):
        coll = self.client[dbname].historics
        query = {
            'email': email
        }
        update = {
            '$push': {
                'scores': {
                    '$each': scores
                }
            }
        }
        proj = {
            '_id': False
        }
        coll.find_one_and_update(query, update, proj, upsert=True)
