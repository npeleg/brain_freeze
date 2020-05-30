import json
from .logger import Logger
from .mongodb import MongoDB
from .service_finder import find_service

logger = Logger(__name__).logger
dbs = {"mongodb": MongoDB}
USER_TABLE = 'users'
SNAPSHOT_TABLE = 'snapshots'


class DBManager:
    def __init__(self, url):
        self.db = find_service(url, dbs)

    def insert_user(self, name, data):
        return self.db.insert(USER_TABLE, name, json.loads(data))

    def insert_snapshot(self, parser_name, data):
        return self.db.insert(SNAPSHOT_TABLE, parser_name, json.loads(data))

    def get_all_users(self):
        return self.db.get_all(USER_TABLE)

    def get_user_data(self, user_id):
        query = {'user_id': user_id}
        return self.db.get(USER_TABLE, query)

    def get_user_snapshots(self, user_id):
        query = {'user_id': user_id}
        distinct_key = 'datetime'
        return self.db.get_one_of_each(SNAPSHOT_TABLE, query, distinct_key)

    def get_available_results(self, user_id, datetime):
        query = {'user_id': user_id, 'datetime': datetime}
        distinct_key = 'result'
        return self.db.get_one_of_each(SNAPSHOT_TABLE, query, distinct_key)

    def get_result(self, user_id, datetime, result_name):
        query = {'user_id': user_id, 'datetime': datetime, 'result': result_name}
        return self.db.get(SNAPSHOT_TABLE, query)

    def _get_result_by_id(self, _id):
        """ for testing: returns the item using its internal id """
        query = {'_id': _id}
        print(query)
        return self.db.get(SNAPSHOT_TABLE, query)
