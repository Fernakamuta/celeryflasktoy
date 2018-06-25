from flask import Blueprint
from flask_restplus import Api, Resource
from webargs.flaskparser import use_kwargs


from .services import Services
from .schemas import SurveySchema, headers_schema


bp_survey = Blueprint('survey', __name__)
api = Api(bp_survey)
services = Services()


@bp_survey.record_once
def on_registration(state):
    services.init_app(state.app.config)


@api.route('/survey')
class Survey(Resource):
    @use_kwargs(headers_schema)
    def get(self, tenant, language, email, groups, **kwargs):
        return services.get_survey(tenant, language, email)

    @use_kwargs(SurveySchema(strict=True))
    @use_kwargs(headers_schema)
    def post(self, tenant, email, survey, groups, **kwargs):
        return services.post_survey(tenant, email, survey, groups)
