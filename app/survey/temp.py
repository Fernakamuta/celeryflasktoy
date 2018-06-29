from copy import deepcopy


def filtered_questions(questions):
    questions_new = [
        question
        for question in questions
        if question['type'] in {'radio-string', 'slide-number'}
    ]
    return questions_new


def filtered_metrics(records):
    records_new = deepcopy(records)
    for metric in records_new:
        for submetric in metric['submetrics']:
            submetric['questions'] = filtered_questions(submetric['questions'])
    return records_new
