from celery import Task, Celery
from pymongo import MongoClient

celery_app = Celery('tasks',
                    broker='amqp://hylmpuuy:mF1Fg953fmSCRHUMjcD-Zw4uMWCM3nQr@skunk.rmq.cloudamqp.com/hylmpuuy')


class MyTask(Task):

    def __init__(self):
        self.name = 'generate_new_report'
        # self.client = MongoClient()

    def run(self, message):
        # db = self.client['testdb']
        # db.test.insert_one(message)
        return message


celery_app.register_task(MyTask())
