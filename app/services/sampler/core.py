import datetime as dt
from random import shuffle

from flatdict import FlatDict


def _newest_date(record):
    """ get newest date from all dates of a dict """
    if isinstance(record, dt.datetime):
        return record
    return max(FlatDict(record).values())


def _sorted_keys(record):
    """
        get 1st level keys sorted from old to new,
        use the newest date for each group,
        break ties randomly
    """
    tuples = [(key, _newest_date(each)) for key, each in record.items()]
    shuffle(tuples)
    tuples.sort(key=lambda x: x[1])
    return [key for key, _ in tuples]


def _select_key(record):
    """ get oldest 1st level key """
    value, *_ = _sorted_keys(record)
    return value


def select_questions(question_dts, n_max):
    metrics = _sorted_keys(question_dts)[:n_max]
    submetrics = [(m, _select_key(question_dts[m])) for m in metrics]
    return [(m, s, _select_key(question_dts[m][s])) for m, s in submetrics]
