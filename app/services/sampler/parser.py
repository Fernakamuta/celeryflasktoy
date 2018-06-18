import datetime as dt

from flatdict import FlatDict


def _question_dts_from_metrics(metrics):
    question_dts = FlatDict()
    for metric in metrics:
        for submetric in metric['submetrics']:
            for question in submetric['questions']:
                m_id = metric['metric_id']
                s_id = submetric['submetric_id']
                q_id = question['question_id']
                question_dts[f'{m_id}:{s_id}:{q_id}'] = dt.datetime(dt.MINYEAR, 1, 1)
    return question_dts.as_dict()


def _question_dts_from_scores(scores):
    question_dts = FlatDict()
    for score in scores:
        m_id = score['metric_id']
        s_id = score['submetric_id']
        q_id = score['question_id']
        key = f'{m_id}:{s_id}:{q_id}'
        date = score['date']
        if key not in question_dts or date > question_dts[key]:
            question_dts[key] = date
    return question_dts.as_dict()


def _merge_question_dts(question_dts_all, question_dts_done):
    questions = FlatDict(question_dts_all)
    question_dts_done = FlatDict(question_dts_done)
    for key in question_dts_done:
        if key in questions:
            questions[key] = question_dts_done[key]
    return questions.as_dict()


def latest_question_dts(metrics, scores):
    question_dts_all = _question_dts_from_metrics(metrics)
    question_dts_done = _question_dts_from_scores(scores)
    return _merge_question_dts(question_dts_all, question_dts_done)


def survey_from_tuples(metrics, tuples):
    metrics_new = {}
    for metric in metrics:
        for submetric in metric['submetrics']:
            for question in submetric['questions']:
                m_id = metric['metric_id']
                s_id = submetric['submetric_id']
                q_id = question['question_id']
                question_new = {
                    **question,
                    'metric_id': m_id,
                    'submetric_id': s_id,
                    'question_id': q_id,
                }
                metrics_new[(m_id, s_id, q_id)] = question_new
    return [metrics_new[(m, s, q)] for m, s, q in tuples]
