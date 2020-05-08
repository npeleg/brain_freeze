import pymongo
from ..logger import Logger

logger = Logger(__name__).logger


class MongoDB:
    def __init__(self, host, port):
        client = pymongo.MongoClient(host=host, port=port)
        self.db = client.db

    def insert_to_table(self, collection, primary_key, data):
        document = {'_id': primary_key, 'data': data}
        self.db[collection].insert_one(document)

    def update_value(self, collection, primary_key, data):
        query = {'_id': primary_key}
        self.db[collection].update_one(query, {'$push': {'data': data}})

    def restore_from_table(self, collection, query):
        return self.db[collection].find_one(query)

    def exists(self, collection, primary_key):
        if self.db[collection].count_documents({'_id': primary_key}, limit=1):
            return True
