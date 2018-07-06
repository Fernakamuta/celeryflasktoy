from celery import Task

from .dao import DataAccessObject
# from .services import 

class FooTask(Task):
    def __init__(self):
        self.dao = None

    def init_app(self, mongo):
        self.dao = DataAccessObject(mongo)
    
    def run(self):
        self.dao.insert_test()