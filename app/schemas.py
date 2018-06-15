from flask import current_app
from jwt import decode, exceptions
from marshmallow import Schema, validates, validates_schema
from webargs import fields, ValidationError

def validate_token(token):
    try:
        secret = current_app.config['JWT_SECRET']
        payload = decode(token, secret)
    except exceptions.DecodeError:
        raise ValidationError('Invalid token', status_code=404)
    return payload


def get_language(country_language):
    if country_language is None:
        return 'pt-br'

    language, country = country_language.split('-', maxsplit=1)

    if language == 'es':
        return 'es-ar'
    return 'pt-br'


class QuestionSchema(Schema):
    question_id = fields.Str(required=True)
    text = fields.Str(required=True)
    type = fields.Str(required=True)
    answers = fields.List(fields.Nested({
        'answer_id': fields.Str(required=True),
        'text': fields.Str(required=True),
        'score': fields.Int(required=True, validate=lambda val: val >= -2 and val <= 2)
    }))
    answered = fields.Nested({
        'answer_id': fields.Str(),
        'text': fields.Str(),
        'score': fields.Int()
    }, allow_none=True)

    @validates_schema
    def validate_answered(self, question):

        if 'answered' not in question:
            raise ValidationError('Missing data for required field.')

        answered = question['answered']
        if answered is not None and answered not in question['answers']:
            raise ValidationError('Invalid data for required field.')


class QuestionsSchema(Schema):
    questions = fields.Nested(QuestionSchema, many=True, required=True)


headers_schema = {
    'user': fields.Function(deserialize=validate_token, load_from='Authorization', location='headers', required=True),
    'language': fields.Function(deserialize=get_language, load_from='Accept-Language', location='headers')
}
