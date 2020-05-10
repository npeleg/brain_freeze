import pymongo
from ..logger import Logger

logger = Logger(__name__).logger


class MongoDB:
    def __init__(self, host, port):
        client = pymongo.MongoClient(host=host, port=port)
        logger.info('creating db')
        self.db = client.db
        db_list = client.list_database_names()
        logger.info("dbs: " + str(db_list))

    def exists(self, collection, primary_key):
        if self.db[collection].count_documents({'_id': primary_key}, limit=1):
            return True
        return False

    def insert_to_table(self, collection, data):
        logger.info(f'inserting data to collection')
        logger.debug(f'inserting data: {data} to collection {collection}')
        self.db[collection].insert_one(data)

    def get_from_table(self, collection, key, value):
        query = {key: value}
        return self.db[collection].find_one(query)

    def get_all_records(self, collection):
        return list(self.db[collection].find({}))

    def get_one_of_each(self, collection, key, value, distinct_key):
        query = {key: value}
        return [x[distinct_key] for x in self.db[collection].find(query).distinct(distinct_key)]
