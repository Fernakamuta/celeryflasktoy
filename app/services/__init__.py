import datetime as dt

from .dao import DataAccessObject
from .sampler import Sampler


def question2score(question, groups, now):

    answered = None
    if question['answered']:
        answered = question['answered']['score']

    score = {
        'metric_id': question['metric_id'],
        'submetric_id': question['submetric_id'],
        'question_id': question['question_id'],
        'group_ids': groups,
        'score': answered,
        'date': now,
    }
    return score


def survey2scores(survey, groups, now):
    return [question2score(question, groups, now) for question in survey]


class Services:
    def __init__(self):
        self.dao = None
        self.sampler = Sampler()

    def init_app(self, config):
        self.dao = DataAccessObject(config)

    def get_survey(self, dbname, lang, email):
        metrics = self.dao.find_metrics(dbname, lang)
        historic = self.dao.find_historic(dbname, email)
        return {'survey': self.sampler.survey(metrics, historic['scores'])}

    def post_survey(self, dbname, email, survey, groups):
        now = dt.datetime.now()
        scores = survey2scores(survey, groups, now)
        self.dao.update_historic(dbname, email, scores)
        return survey
