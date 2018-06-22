import numpy as np

from flatdict import FlatDict


def _avg_weighted(tuples):
    values = [value for value, date in tuples if value is not None]
    if values:
        return np.mean(values)
    return None


def _avg(record):
    record_flat = FlatDict(record)
    values = [value for value in record_flat.values() if value is not None]
    if values:
        return np.mean(values)
    return None


def _compute_sole_scores(record):
    # questions
    record_q = {
        f'{mk}:{sk}:{qk}': _avg_weighted(tuples)
        for mk, mv in record.items()
        for sk, sv in mv.items()
        for qk, tuples in sv.items()
    }
    record_q = FlatDict(record_q).as_dict()

    # sub-metrics
    record_s = {
        f'{mk}:{sk}': _avg(sv)
        for mk, mv in record_q.items()
        for sk, sv in mv.items()
    }
    record_s = FlatDict(record_s).as_dict()

    # metrics
    record_m = {
        mk: _avg(mv)
        for mk, mv in record_s.items()
    }
    record_m = FlatDict(record_m).as_dict()

    return record_m


def _compute_group_scores(metric_ids, record_m):
    avgs = {}
    for m in metric_ids:
        values = [each[m] for each in record_m if m in each and each[m] is not None]
        avgs[m] = np.mean(values) if values else None
    return avgs


def _compute_overall(record_m):
    values = [v for v in record_m.values() if v is not None]
    if values:
        return np.mean(values)
    return None


def compute_scores(metric_ids, records):
    records_m = [_compute_sole_scores(each) for each in records]
    record_m = _compute_group_scores(metric_ids, records_m)
    overall = _compute_overall(record_m)
    return overall, record_m
