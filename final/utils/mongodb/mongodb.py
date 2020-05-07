import pymongo
# from ...utils import Logger

# logger = Logger(__name__).logger


class MongoDB:
    def __init__(self, host, port):
        client = pymongo.MongoClient(host=host, port=port)
        self.db = client.db

    def insert_to_table(self, collection, document):
        self.db[collection].insert_one(document)

    def update_value(self, collection, key, data):
        self.db[collection].update_one({key, data})

    def restore_from_table(self, collection, query):
        return self.db[collection].find_one(query)

# if db.collection.count_documents({'UserIDS': newID}, limit=1):
