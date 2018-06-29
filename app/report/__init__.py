import datetime as dt

from .dao import DataAccessObject
from .stats import get_report


class ReportService:
    def __init__(self):
        self.dao = None

    def init_app(self, mongo):
        self.dao = DataAccessObject(mongo)

    def get(self, dbname, group_id):
        now = dt.datetime.now()
        date = now.replace(minute=0, second=0, microsecond=0)
        report = self.dao.find_report(dbname, group_id, date)
        return {'report': report}

    def post(self, dbname, group_id):
        metric_ids = self.dao.find_metric_ids(dbname)
        scores = self.dao.find_scores_by_group(dbname, group_id)
        report = get_report(group_id, metric_ids, scores)
        self.dao.replace_report(dbname, report)
