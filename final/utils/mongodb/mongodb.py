import pymongo
from ..logger import Logger

logger = Logger(__name__).logger


class MongoDB:
    def __init__(self, host, port):
        client = pymongo.MongoClient(host=host, port=port)
        self.db = client.db

    def insert(self, collection, data):
        logger.info(f'inserting data to collection')
        logger.debug(f'inserting data: {data} to collection {collection}')
        self.db[collection].insert_one(data)

    def _get_general(self, collection, query, distinct_key):
        if query != {}:
            lst = []
            for key, value in query.items():
                lst.append({key: value})
            query = {"$and": lst}
        if distinct_key:
            return self.db[collection].find(query).distinct(distinct_key)
        else:
            result = self.db[collection].find_one(query)
            print(result)
            if result:
                del result['_id']
            return result

    def get(self, collection, query):
        return self._get_general(collection, query, None)

    def get_one_of_each(self, collection, query, distinct_key):
        return self._get_general(collection, query, distinct_key)

    def get_all(self, collection):
        return list(self.db[collection].find({}))
