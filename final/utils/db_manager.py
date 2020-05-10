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

    def insert_user(self, data):
        self.db.insert_to_table(USER_TABLE, data)

    def insert_snapshot(self, data):
        self.db.insert_to_table(SNAPSHOT_TABLE, data)

    def get_all_users(self):
        primary_key = 'user_id'
        return self.db.get_all_records(USER_TABLE, primary_key)

    def get_user_data(self, user_id):
        key = 'user_id'
        value = user_id
        return self.db.get_from_table(USER_TABLE, key, value)

    def get_user_snapshots(self, user_id):
        key = 'user_id'
        value = user_id
        distinct_key = 'datetime'
        return self.db.get_one_of_each(SNAPSHOT_TABLE, key, value, distinct_key)
