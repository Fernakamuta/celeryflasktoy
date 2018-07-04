import atexit

from flask import Blueprint
from flask_restplus import Api, Resource
from webargs.flaskparser import use_kwargs
from pymongo import MongoClient

from .survey import SurveyService
from .report import ReportService
from .schemas import SurveySchema, headers_schema, headers_report


bp_survey = Blueprint('survey', __name__)
api = Api(bp_survey)
survey_service = SurveyService()
report_service = ReportService()


def close_mongo(mongo):
    mongo.close()
    print('MongoDB disconnected.')


@bp_survey.record_once
def on_registration(state):
    mongo = MongoClient(state.app.config['MONGO_URL'])
    survey_service.init_app(mongo)
    report_service.init_app(mongo)
    print(f' * MongoDB is Connected on {mongo.HOST}:{mongo.PORT}')
    atexit.register(close_mongo, mongo)


@api.route('/survey')
class Survey(Resource):
    @use_kwargs(headers_schema)
    def get(self, tenant, language, email, **kwargs):
        return survey_service.get(tenant, language, email)

    @use_kwargs(SurveySchema(strict=True))
    @use_kwargs(headers_schema)
    def post(self, tenant, email, survey, groups, **kwargs):
        payload = survey_service.post(tenant, email, survey, groups)
        for group_id in groups:
            report_service.post(tenant, group_id)
        return payload


@api.route('/reports/<string:group_id>')
class Reports(Resource):
    @use_kwargs(headers_report)
    def get(self, group_id, tenant):
        return report_service.get(group_id, tenant)
