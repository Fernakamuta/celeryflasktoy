from pymongo import MongoClient


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
    def __init__(self):
        self.client = None

    def init_app(self, config):
        self.client = MongoClient(config['MONGO_URL'])

    def survey_example(self):
        cursor = self.client['survey-test']['survey_example'].find()
        record, *_ = list(cursor)
        return stringfy_id(record)

    def find_metrics(self, dbname, lang):
        cursor = self.client[dbname].metrics.find()
        records = parse_i18n(list(cursor), lang)
        return [stringfy_id(each) for each in records]
