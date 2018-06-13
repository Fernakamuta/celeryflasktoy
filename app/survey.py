from flask import Blueprint
from flask_restplus import Api, Resource

from .dao import DataAccessObject


bp_survey = Blueprint('survey', __name__)
api = Api(bp_survey, doc='/swagger/')
dao = DataAccessObject()


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
        return dao.find_temp()

    def post(self):
        return dao.find_temp()
