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

        payload = {
            'questions': [
                {
                    'question_id': 'A',
                    'text': 'example1',
                    'type': 'radio-string',
                    'answers': [
                        {
                            'answer_id': 'A1',
                            'text': 'Discordo Totalmente',
                            'score': -2
                        },
                        {
                            'answer_id': 'A2',
                            'text': 'Discordo',
                            'score': -1
                        },
                        {
                            'answer_id': 'A3',
                            'text': 'Neutro',
                            'score': 0
                        },
                        {
                            'answer_id': 'A4',
                            'text': 'Concordo',
                            'score': 1
                        },
                        {
                            'answer_id': 'A5',
                            'text': 'Concordo Plenamente',
                            'score': 2
                        },
                    ],
                    'answered': None
                },
                {
                    'id': 'B',
                    'text': 'Estou apropriadamente envolvido em decisões que afetam meu trabalho.',
                    'type': 'slide-number',
                    'answers': [
                        {
                            'answer_id': 'B0',
                            'text': 'Discordo Totalmente',
                            'score': -2
                        },
                        {
                            'answer_id': 'B1',
                            'text': 'Discordo',
                            'score': -1
                        },
                        {
                            'answer_id': 'B2',
                            'text': 'Neutro',
                            'score': 0
                        },
                        {
                            'answer_id': 'B3',
                            'text': 'Concordo',
                            'score': 1
                        },
                        {
                            'answer_id': 'B4',
                            'text': 'Concordo Plenamente',
                            'score': 2
                        }
                    ],
                    'answered': None
                },
            ]
        }
        self.client['survey-test']['temp'].drop()
        self.client['survey-test']['temp'].insert(payload)

    def find_temp(self):
        cursor = self.client['master']['temp'].find()
        record = [each for each in cursor][0]
        return stringfy_id(record)
