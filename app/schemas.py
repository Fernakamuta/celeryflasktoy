import json

from marshmallow import (
    Schema,
    validates_schema,
    ValidationError
)
from marshmallow.fields import Str, Function, Int, List
from webargs.fields import Nested


def get_language(country_language):
    if country_language is None:
        return 'pt-br'
    if country_language[:2] == 'es':
        return 'es-ar'
    return 'pt-br'


class QuestionSchema(Schema):
    question_id = Str(required=True)
    text = Str(required=True)
    type = Str(required=True)
    answers = List(Nested({
        'answer_id': Str(required=True),
        'text': Str(required=True),
        'score': Int(required=True, validate=lambda val: val >= -2 and val <= 2)
    }))
    answered = Nested({
        'answer_id': Str(),
        'text': Str(),
        'score': Int()
    }, allow_none=True)

    @validates_schema
    def validate_answered(self, question):

        if 'answered' not in question:
            raise ValidationError('Missing data for required field.')

        answered = question['answered']
        if answered is not None and answered not in question['answers']:
            raise ValidationError('Invalid data for required field.')


class SurveySchema(Schema):
    survey = Nested(QuestionSchema, many=True, required=True)


headers_schema = {
    'email': Str(required=True, load_from='Email', location='headers'),
    'tenant': Str(required=True, load_from='Tenant', location='headers'),
    'language': Function(deserialize=get_language, missing='pt-br', load_from='Accept-Language', location='headers')
}
