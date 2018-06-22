import datetime as dt
from collections import defaultdict

from flatdict import FlatDict


def _to_record(scores):
    record = defaultdict(list)
    for each in scores:
        m = each['metric_id']
        s = each['submetric_id']
        q = each['question_id']
        score_value = each['score']
        score_date = each['date']
        record[f'{m}:{s}:{q}'] += [(score_value, score_date)]
    return FlatDict(record).as_dict()


def scores2records(scores):
    mapper = defaultdict(list)
    for score in scores:
        email = score['email']
        mapper[email].append(score)
    return [_to_record(each) for each in mapper.values()]


def to_report(group_id, metric_ids, overall, scores_m):
    now = dt.datetime.now()
    scores = {
        **{key: None for key in metric_ids},
        **scores_m,
    }
    metrics = [{'metric_id': k, 'score': v} for k, v in scores.items()]
    report = {
        'group_id': group_id,
        'date': now.replace(minute=0, second=0, microsecond=0),
        'metrics': metrics,
        'score': overall,
    }
    return report
