import datetime as dt

from app.report.stats.parser import to_report, scores2records
from app.report.stats.core import compute_scores


def filtered_scores(scores):
    start_dt = dt.datetime.now() - dt.timedelta(days=90)
    return [score for score in scores if start_dt < score['date']]


def get_report(group_id, metric_ids, scores):

    # filter
    scores = filtered_scores(scores)

    # parse to user records
    records = scores2records(scores)

    # compute
    overall, record_m = compute_scores(metric_ids, records)

    # parse out
    return to_report(group_id, metric_ids, overall, record_m)
