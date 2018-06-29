import datetime as dt

from .dao import DataAccessObject
from .sampler import Sampler


def question2score(question, email, group_ids, now):
    score, answer_id, feedback = None, None, None
    if question['answered']:
        score = question['answered']['score']
        answer_id = question['answered']['answer_id']
        if 'feedback_answer' in question['answered']:
            feedback = question['answered']['feedback_answer']

    score = {
        'metric_id': question['metric_id'],
        'submetric_id': question['submetric_id'],
        'question_id': question['question_id'],
        'answer_id': answer_id,
        'group_ids': group_ids,
        'score': score,
        'feedback': feedback,
        'date': now,
        'email': email,
    }
    return score


def survey2scores(survey, email, group_ids, now):
    return [question2score(question, email, group_ids, now) for question in survey]


class SurveyService:
    def __init__(self):
        self.dao = None
        self.sampler = Sampler()

    def init_app(self, mongo):
        self.dao = DataAccessObject(mongo)

    def get(self, dbname, lang, email):
        metrics = self.dao.find_metrics(dbname, lang)
        scores = self.dao.find_scores(dbname, email)
        return {'survey': self.sampler.survey(metrics, scores)}

    def post(self, dbname, email, survey, group_ids):
        now = dt.datetime.now()
        scores = survey2scores(survey, email, group_ids, now)
        self.dao.insert_scores(dbname, scores)
        return survey
