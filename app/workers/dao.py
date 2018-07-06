import pymongo


class DataAccessObject:
    def __init__(self, mongo):
        self.client = mongo

    def insert_test(self):
        db = self.client['test'].testecol.insert({'test': 'teste'})

    def replace_report(self, dbname, report):
        query = {
            'group_id': report['group_id'],
            'date': report['date'],
        }
        self.client[dbname].reports.replace_one(query, report, upsert=True)
