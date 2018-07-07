import pymongo


class DataAccessObject:
    def __init__(self, mongo):
        self.client = mongo

    def insert_test(self, message):
        self.client['test'].testecol.insert(message)