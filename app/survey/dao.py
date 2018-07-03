from pymongo import MongoClient

from app.survey.temp import filtered_metrics


def parse_i18n(record, lang):
    default = 'pt-br'
    if isinstance(record, list):
        return [parse_i18n(each, lang) for each in record]
    if isinstance(record, dict):
        if not {lang, default} & set(record):
            return {key: parse_i18n(value, lang) for key, value in record.items()}
        return record.get(lang, record[default])
    return record


class DataAccessObject:
    def __init__(self, mongo):
        self.client = mongo

    def find_metrics(self, dbname, lang):
        cursor = self.client[dbname].metrics.find({}, {'_id': False})

        # temporary filter
        records = filtered_metrics(list(cursor))

        return parse_i18n(records, lang)

    def find_scores(self, dbname, email):
        query = {
            'email': email
        }
        proj = {
            '_id': False
        }
        cursor = self.client[dbname].answers.find(query, proj)
        return list(cursor)

    def insert_scores(self, dbname, scores):
        self.client[dbname].answers.insert_many(scores)
