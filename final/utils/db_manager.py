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

    def insert_user(self, primary_key, data):
        self.db.insert_to_table(USER_TABLE, primary_key, data)
        self.db.insert_to_table(SNAPSHOT_TABLE, primary_key, data=[])

    def insert_snapshot(self, primary_key, new_data):
        self.db.update_value(SNAPSHOT_TABLE, primary_key, new_data)
