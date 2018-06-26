from marshmallow import (
    Schema,
    validate,
    validates_schema,
    post_load,
    ValidationError
)
from marshmallow.fields import Str, Function, Int, List, Float
from webargs.fields import Nested


class QuestionSchema(Schema):
    metric_id = Str(required=True)
    submetric_id = Str(required=True)
    question_id = Str(required=True)
    text = Str(required=True)
    type = Str(required=True)
    answers = List(Nested({
        'answer_id': Str(required=True),
        'text': Str(required=True),
        'score': Float(required=True, validate=validate.OneOf([-2, -1, 0, 1, 2]))
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
    
    @post_load
    def clean_feedbacks(self, data):
        print('DATA:')



def get_language(country_language):
    if country_language is None:
        return 'pt-br'
    if country_language[:2] == 'es':
        return 'es-ar'
    return 'pt-br'


def get_groups(groups):
    return groups.split(',')


headers_schema = {
    'email': Str(required=True, load_from='Email', location='headers'),
    'tenant': Str(required=True, load_from='Tenant', location='headers'),
    'groups': Function(required=True, deserialize=get_groups, load_from='Groups', location='headers'),
    'language': Function(deserialize=get_language, missing='pt-br', load_from='Accept-Language', location='headers'),
}
