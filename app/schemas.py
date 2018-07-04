from marshmallow import (
    Schema,
    validate,
    validates,
    validates_schema,
    ValidationError
)
from marshmallow.fields import Str, Function, Int, List, Float, Boolean
from webargs.fields import Nested
from copy import deepcopy


class QuestionSchema(Schema):
    metric_id = Str(required=True)
    metric_label = Str(required=True)
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
        'feedback': Str(),
        'feedback_answer': Nested({
            'text': Str(required=True),
            'is_annonymous': Boolean(required=True)
        }, allow_none=True)
    }, allow_none=True, required=True)

    @staticmethod
    def _has_duplicated(answers):
        unique_answers = set([tuple(answer.items()) for answer in answers])
        return len(answers) != len(unique_answers)

    @staticmethod
    def _get_answers(question):
        return question['answered'], question['answers']

    @staticmethod
    def _has_feedback(answers):
        for answer in answers:
            if 'feedback' not in answer:
                return False
        return True

    def _is_subset(self, answered, answers):
        answered = deepcopy(answered)

        if self._has_feedback(answers):
            del answered['feedback_answer']

        return answered in answers

    @validates('answers')
    def validate_answers(self, answers):
        has_duplicated = self._has_duplicated(answers)
        if has_duplicated:
            raise ValidationError('Invalid answers array.')

    @validates_schema(skip_on_field_errors=True)
    def validate_answered(self, question):
        answered, answers = self._get_answers(question)

        # Allows skip question
        if not answered:
            return

        has_feedback = self._has_feedback(answers)
        if has_feedback:
            if not set(answered) >= {'feedback', 'feedback_answer'}:
                raise ValidationError('Missing feedback or feedback_answer.')

            if not answered['feedback_answer'] is None:
                incomplete_feedback = not set(answered['feedback_answer']) >= {'text', 'is_annonymous'}
                if incomplete_feedback:
                    raise ValidationError('Missing fields text or is_annonnymous at feedback_answer.')

        is_answered_subset = self._is_subset(answered, answers)
        if not is_answered_subset:
            raise ValidationError('Invalid answered.')


class SurveySchema(Schema):
    survey = Nested(QuestionSchema, many=True, required=True)


def get_language(country_language):
    if country_language is None:
        return 'pt-br'
    if country_language[:2] == 'es':
        return 'es-ar'
    return 'pt-br'


def get_groups(groups):
    return groups.replace(' ', '').split(',')


headers_schema = {
    'email': Str(required=True, load_from='Email', location='headers'),
    'tenant': Str(required=True, load_from='Tenant', location='headers'),
    'groups': Function(required=True, deserialize=get_groups, load_from='Groups', location='headers'),
    'language': Function(deserialize=get_language, missing='pt-br', load_from='Accept-Language', location='headers'),
}

headers_report = {
    'tenant': Str(required=True, load_from='Tenant', location='headers'),
}
