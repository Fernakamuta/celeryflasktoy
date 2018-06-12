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
        pass
        # self.client = MongoClient(host=config['MONGO_HOST'], port=config['MONGO_PORT'])
        # # if config.MONGO_AUTH == 'true':
        # #     mongo.leads.authenticate(config.MONGO_USER, config.MONGO_PASS)
        #
        # payload = {
        #     'questions': [
        #         {
        #             'id': '1',
        #             'text': 'Estou apropriadamente envolvido em decisões que afetam meu trabalho.',
        #             'type': 'radio-string',
        #             'answers': [
        #                 {
        #                     'id': 'sadas979gsa9g6',
        #                     'text': 'Discordo Totalmente',
        #                     'score': -2
        #                 },
        #                 {
        #                     'id': '3423246',
        #                     'text': 'Discordo',
        #                     'score': -1
        #                 },
        #                 {
        #                     'id': '345hkjfhsdf',
        #                     'text': 'Neutro',
        #                     'score': 0
        #                 },
        #                 {
        #                     'id': 'sdb7fd876g',
        #                     'text': 'Concordo',
        #                     'score': 1
        #                 },
        #                 {
        #                     'id': 'bvcbcvb098096',
        #                     'text': 'Concordo Plenamente',
        #                     'score': 2
        #                 }
        #             ],
        #             'answered': None
        #         },
        #         {
        #             'id': '2',
        #             'text': 'Tenho orgulho do que minha empresa representa.',
        #             'type': 'radio-string',
        #             'answers': [
        #                 {
        #                     'id': 'sadas979gsa9g6',
        #                     'text': 'Discordo Totalmente',
        #                     'score': -2
        #                 },
        #                 {
        #                     'id': '3423246',
        #                     'text': 'Discordo',
        #                     'score': -1
        #                 },
        #                 {
        #                     'id': '345hkjfhsdf',
        #                     'text': 'Neutro',
        #                     'score': 0
        #                 },
        #                 {
        #                     'id': 'sdb7fd876g',
        #                     'text': 'Concordo',
        #                     'score': 1
        #                 },
        #                 {
        #                     'id': 'bvcbcvb098096',
        #                     'text': 'Concordo Plenamente',
        #                     'score': 2
        #                 }
        #             ],
        #             'answered': None
        #         },
        #         {
        #             'id': '3',
        #             'text': 'Sinto que meu trabalho tem um propósito.',
        #             'type': 'radio-string',
        #             'answers': [
        #                 {
        #                     'id': 'sadas979gsa9g6',
        #                     'text': 'Discordo Totalmente',
        #                     'score': -2
        #                 },
        #                 {
        #                     'id': '3423246',
        #                     'text': 'Discordo',
        #                     'score': -1
        #                 },
        #                 {
        #                     'id': '345hkjfhsdf',
        #                     'text': 'Neutro',
        #                     'score': 0
        #                 },
        #                 {
        #                     'id': 'sdb7fd876g',
        #                     'text': 'Concordo',
        #                     'score': 1
        #                 },
        #                 {
        #                     'id': 'bvcbcvb098096',
        #                     'text': 'Concordo Plenamente',
        #                     'score': 2
        #                 }
        #             ],
        #             'answered': None
        #         },
        #         {
        #             'id': '4',
        #             'text': 'Eu me considero um promotor da empresa.',
        #             'type': 'radio-string',
        #             'answers': [
        #                 {
        #                     'id': 'sadas979gsa9g6',
        #                     'text': 'Discordo Totalmente',
        #                     'score': -2
        #                 },
        #                 {
        #                     'id': '3423246',
        #                     'text': 'Discordo',
        #                     'score': -1
        #                 },
        #                 {
        #                     'id': '345hkjfhsdf',
        #                     'text': 'Neutro',
        #                     'score': 0
        #                 },
        #                 {
        #                     'id': 'sdb7fd876g',
        #                     'text': 'Concordo',
        #                     'score': 1
        #                 },
        #                 {
        #                     'id': 'bvcbcvb098096',
        #                     'text': 'Concordo Plenamente',
        #                     'score': 2
        #                 }
        #             ],
        #             'answered': None
        #         },
        #         {
        #             'id': '5',
        #             'text': 'Minha empresa celebra nossas conquistas e aprendizados.',
        #             'type': 'radio-string',
        #             'answers': [
        #                 {
        #                     'id': 'sadas979gsa9g6',
        #                     'text': 'Discordo Totalmente',
        #                     'score': -2
        #                 },
        #                 {
        #                     'id': '3423246',
        #                     'text': 'Discordo',
        #                     'score': -1
        #                 },
        #                 {
        #                     'id': '345hkjfhsdf',
        #                     'text': 'Neutro',
        #                     'score': 0
        #                 },
        #                 {
        #                     'id': 'sdb7fd876g',
        #                     'text': 'Concordo',
        #                     'score': 1
        #                 },
        #                 {
        #                     'id': 'bvcbcvb098096',
        #                     'text': 'Concordo Plenamente',
        #                     'score': 2
        #                 }
        #             ],
        #             'answered': None
        #         }
        #     ]
        # }
        # self.client['master']['temp'].drop()
        # self.client['master']['temp'].insert(payload)

    def find_temp(self):
        cursor = self.client['master']['temp'].find()
        record = [each for each in cursor][0]
        return stringfy_id(record)
