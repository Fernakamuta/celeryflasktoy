from flask import Blueprint
from flask_restplus import Api, Resource

from .dao import DataAccessObject


bp_survey = Blueprint('survey', __name__)
api = Api(bp_survey, doc='/swagger/')
dao = DataAccessObject()


payload = {
    'questions': [
        {
            'id': '1',
            'text': 'Estou apropriadamente envolvido em decisões que afetam meu trabalho.',
            'type': 'radio-string',
            'answers': [
                {
                    'id': 'sadas979gsa9g6',
                    'text': 'Discordo Totalmente',
                    'score': -2
                },
                {
                    'id': '3423246',
                    'text': 'Discordo',
                    'score': -1
                },
                {
                    'id': '345hkjfhsdf',
                    'text': 'Neutro',
                    'score': 0
                },
                {
                    'id': 'sdb7fd876g',
                    'text': 'Concordo',
                    'score': 1
                },
                {
                    'id': 'bvcbcvb098096',
                    'text': 'Concordo Plenamente',
                    'score': 2
                }
            ],
            'answered': None
        },
        {
            'id': '2',
            'text': 'Tenho orgulho do que minha empresa representa.',
            'type': 'radio-string',
            'answers': [
                {
                    'id': 'sadas979gsa9g6',
                    'text': 'Discordo Totalmente',
                    'score': -2
                },
                {
                    'id': '3423246',
                    'text': 'Discordo',
                    'score': -1
                },
                {
                    'id': '345hkjfhsdf',
                    'text': 'Neutro',
                    'score': 0
                },
                {
                    'id': 'sdb7fd876g',
                    'text': 'Concordo',
                    'score': 1
                },
                {
                    'id': 'bvcbcvb098096',
                    'text': 'Concordo Plenamente',
                    'score': 2
                }
            ],
            'answered': None
        },
        {
            'id': '3',
            'text': 'Sinto que meu trabalho tem um propósito.',
            'type': 'radio-string',
            'answers': [
                {
                    'id': 'sadas979gsa9g6',
                    'text': 'Discordo Totalmente',
                    'score': -2
                },
                {
                    'id': '3423246',
                    'text': 'Discordo',
                    'score': -1
                },
                {
                    'id': '345hkjfhsdf',
                    'text': 'Neutro',
                    'score': 0
                },
                {
                    'id': 'sdb7fd876g',
                    'text': 'Concordo',
                    'score': 1
                },
                {
                    'id': 'bvcbcvb098096',
                    'text': 'Concordo Plenamente',
                    'score': 2
                }
            ],
            'answered': None
        },
        {
            'id': '4',
            'text': 'Eu me considero um promotor da empresa.',
            'type': 'radio-string',
            'answers': [
                {
                    'id': 'sadas979gsa9g6',
                    'text': 'Discordo Totalmente',
                    'score': -2
                },
                {
                    'id': '3423246',
                    'text': 'Discordo',
                    'score': -1
                },
                {
                    'id': '345hkjfhsdf',
                    'text': 'Neutro',
                    'score': 0
                },
                {
                    'id': 'sdb7fd876g',
                    'text': 'Concordo',
                    'score': 1
                },
                {
                    'id': 'bvcbcvb098096',
                    'text': 'Concordo Plenamente',
                    'score': 2
                }
            ],
            'answered': None
        },
        {
            'id': '5',
            'text': 'Minha empresa celebra nossas conquistas e aprendizados.',
            'type': 'radio-string',
            'answers': [
                {
                    'id': 'sadas979gsa9g6',
                    'text': 'Discordo Totalmente',
                    'score': -2
                },
                {
                    'id': '3423246',
                    'text': 'Discordo',
                    'score': -1
                },
                {
                    'id': '345hkjfhsdf',
                    'text': 'Neutro',
                    'score': 0
                },
                {
                    'id': 'sdb7fd876g',
                    'text': 'Concordo',
                    'score': 1
                },
                {
                    'id': 'bvcbcvb098096',
                    'text': 'Concordo Plenamente',
                    'score': 2
                }
            ],
            'answered': None
        }
    ]
}


@bp_survey.record_once
def on_registration(state):
    dao.init_app(state.app.config)


@api.route('/survey')
class Survey(Resource):
    def get(self):
        payload_in = {
            'id': 'test_id',
            'user': 'test_email',
            'profile': 'test_profile',
            'role': 'test_role',
        }
        return payload

    def post(self):
        return payload
