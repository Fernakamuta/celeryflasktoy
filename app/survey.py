from flask import Blueprint
from flask_restplus import Api, Resource

from app.services import Services


bp_survey = Blueprint('survey', __name__)
api = Api(bp_survey)
services = Services()


@bp_survey.record_once
def on_registration(state):
    services.init_app(state.app.config)


@api.route('/survey')
class Survey(Resource):
    def get(self):
        return services.get_survey('survey-test', 'pt-br', 'test@test.com')

    def post(self):
        return services.post_survey('survey-test', 'pt-br', 'test@test.com', {})

