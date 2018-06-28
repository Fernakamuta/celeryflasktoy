from marshmallow import (
    Schema,
    validate,
    validates_schema,
    ValidationError
)
from marshmallow.fields import Str, Function, Int, List, Float, Boolean
from webargs.fields import Nested


class QuestionSchema(Schema):
    metric_id = Str(required=True)
    submetric_id = Str(required=True)
    question_id = Str(required=True)
    text = Str(required=True)
    type = Str(required=True)
    answers = List(Nested({
        'feedback': Str(),
        'answer_id': Str(required=True),
        'text': Str(required=True),
        'score': Float(required=True, validate=validate.OneOf([-2, -1, 0, 1, 2]))
    }), required=True)
    answered = Nested({
        'answer_id': Str(required=True),
        'text': Str(required=True),
        'score': Int(required=True),
        'feedback': Nested({
            'question': Str(required=True),
            'answer': Str(required=True),
            'isAnnonymous': Boolean(required=True)
        }, allow_none=True)
    }, allow_none=True, strict=True, required=True)

    @staticmethod
    def _get_answers(question):
        return question['answered'], question['answers']

    @staticmethod
    def _has_feedback(answers):
        for answer in answers:
            if 'feedback' not in answer:
                return False
        return True

    @staticmethod
    def _remove_feedback(answer):
        answer_new = {**answer}
        del answer_new['feedback']
        return answer_new

    @staticmethod
    def _get_original(answer):
        answer_original = {
            **answer,
            'feedback' : answer['feedback']['question']
        }
        return answer_original


    @validates_schema(skip_on_field_errors=True)
    def validate_answered(self, question):
        answered, answers = self._get_answers(question)

        # Allows skip question
        if answered == None:
            return

        has_feedback = self._has_feedback(answers)

        if has_feedback:
        # Validates Answered
            if 'feedback' not in answered:
                raise ValidationError('Missing feedback for answer.')

            none_feedback = answered['feedback'] == None

            if none_feedback:
                answers = [self._remove_feedback(answer) for answer in answers]
                answered = self._remove_feedback(answered)
            else:
                answered = self._get_original(answered)

        if answered not in answers:
            raise ValidationError('Invalid answer.') 


class SurveySchema(Schema):
    survey = Nested(QuestionSchema, many=True, required=True)


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
