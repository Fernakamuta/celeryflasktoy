from flask import Blueprint
from flask_restplus import Api, Resource
from webargs.flaskparser import use_kwargs


from .services import Services
from .schemas import QuestionsSchema, headers_schema


bp_survey = Blueprint('survey', __name__)
api = Api(bp_survey)
services = Services()


@bp_survey.record_once
def on_registration(state):
    services.init_app(state.app.config)


@api.route('/survey')
class Survey(Resource):
    @use_kwargs(headers_schema)
    def get(self, user, language):
        return services.get_survey('survey-test', language, user['user'])

    @use_kwargs(QuestionsSchema(strict=True))
    @use_kwargs(headers_schema)
    def post(self, user, language, questions):
        return services.post_survey('survey-test', 'pt-br', 'test@test.com', {})
