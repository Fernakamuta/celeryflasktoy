from .dao import DataAccessObject
from .sampler import Sampler


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

    def post_survey(self, dbname, email, payload):
        return payload
