

class DataAccessObject:
    def __init__(self, mongo):
        self.client = mongo

    def find_metric_ids(self, dbname):
        cursor = self.client[dbname].metrics.find()
        return [each['metric_id'] for each in cursor]

    def replace_report(self, dbname, report):
        query = {
            'group_id': report['group_id'],
            'date': report['date'],
        }
        self.client[dbname].reports.replace_one(query, report, upsert=True)

    def find_scores_by_group(self, dbname, group_id):
        query = {
            'group_ids': group_id
        }
        proj = {
            '_id': False
        }
        cursor = self.client[dbname].historics.find(query, proj)
        return list(cursor)

    def find_report(self, dbname, group_id, date):
        query = {
            'group_id': group_id,
            'date': date,
        }
        proj = {
            '_id': False,
            'date': False,
        }
        return self.client[dbname].reports.find_one(query, proj)
