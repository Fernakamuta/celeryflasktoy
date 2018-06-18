import datetime as dt
from random import shuffle

from flatdict import FlatDict


example = [
    {
        "question_id": "A",
        "text": "exampleA",
        "type": "radio-string",
        "answers": [
            {
                "answer_id": "A1",
                "text": "Discordo Totalmente",
                "score": -2
            },
            {
                "answer_id": "A2",
                "text": "Discordo",
                "score": -1
            },
            {
                "answer_id": "A3",
                "text": "Neutro",
                "score": 0
            },
            {
                "answer_id": "A4",
                "text": "Concordo",
                "score": 1
            },
            {
                "answer_id": "A5",
                "text": "Concordo Plenamente",
                "score": 2
            }
        ],
        "answered": None
    },
    {
        "id": "B",
        "text": "ExampleB",
        "type": "slide-number",
        "answers": [
            {
                "answer_id": "B0",
                "text": "Discordo Totalmente",
                "score": -2
            },
            {
                "answer_id": "B1",
                "text": "Discordo",
                "score": -1
            },
            {
                "answer_id": "B2",
                "text": "Neutro",
                "score": 0
            },
            {
                "answer_id": "B3",
                "text": "Concordo",
                "score": 1
            },
            {
                "answer_id": "B4",
                "text": "Concordo Plenamente",
                "score": 2
            }
        ],
        "answered": None
    },
]


def newest_date(record):
    """ get newest date from all dates of a dict """
    if isinstance(record, dt.datetime):
        return record
    return max(FlatDict(record).values())


def sorted_keys(record):
    """
        get 1st level keys sorted from old to new,
        use the newest date for each group,
        break ties randomly
    """
    tuples = [(key, newest_date(each)) for key, each in record.items()]
    shuffle(tuples)
    tuples.sort(key=lambda x: x[1])
    return [key for key, _ in tuples]


def select_key(record):
    """ get oldest 1st level key """
    value, *_ = sorted_keys(record)
    return value


class Sampler:
    @staticmethod
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

    @staticmethod
    def _question_dts_from_historic(historic):
        question_dts = FlatDict()
        for score in historic['scores']:
            m_id = score['metric_id']
            s_id = score['submetric_id']
            q_id = score['question_id']
            question_dts[f'{m_id}:{s_id}:{q_id}'] = score['date']
        return question_dts.as_dict()

    @staticmethod
    def _merge_question_dts(question_dts_all, question_dts_done):
        questions = FlatDict(question_dts_all)
        question_dts_done = FlatDict(question_dts_done)
        for key in question_dts_done:
            if key in questions:
                questions[key] = question_dts_done[key]
        return questions.as_dict()

    @staticmethod
    def _select_questions(question_dts, n_max):
        metrics = sorted_keys(question_dts)[:n_max]
        submetrics = [(m, select_key(question_dts[m])) for m in metrics]
        return [(m, s, select_key(question_dts[m][s])) for m, s in submetrics]

    @staticmethod
    def _survey_from_tuples(metrics, tuples):
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

    def survey(self, metrics, historic):

        # extract mappers from payloads
        question_dts_all = self._question_dts_from_metrics(metrics)
        question_dts_done = self._question_dts_from_historic(historic)
        question_dts = self._merge_question_dts(question_dts_all, question_dts_done)

        # select questions
        n_max = 5 if question_dts_done else 10
        tuples = self._select_questions(question_dts, n_max)

        # build payload from tuples
        return self._survey_from_tuples(metrics, tuples)
