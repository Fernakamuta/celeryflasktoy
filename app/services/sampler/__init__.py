from .parser import latest_question_dts, survey_from_tuples
from .core import select_questions


class Sampler:
    @staticmethod
    def survey(metrics, scores):
        n_max = 5 if scores else 10
        question_dts = latest_question_dts(metrics, scores)
        tuples = select_questions(question_dts, n_max)
        return survey_from_tuples(metrics, tuples)
