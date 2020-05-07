import threading
from ..utils import find_service, Logger, MQManager, DBManager

logger = Logger(__name__).logger
parser_names = {'pose', 'feelings'}
lock = threading.Lock()


def wrap_saver(db, content):
    """ returns a function that saves data to the relevant table in the db """
    def save_user_to_db(data):
        with lock:
            logger.info('sent user data to save in db')
        db.insert_user(data)

    def save_snapshot_to_db(data):
        with lock:
            logger.info('sent snapshot data to save in db')
        db.insert_snapshot(data)
    
    if content == 'user':
        return save_user_to_db
    elif content == 'snapshot':
        return save_snapshot_to_db


class Saver:
    def __init__(self, url):
        self.db = DBManager(url)

    def save(self, parser_name, data):
        if data is None:
            return
        self.db.insert_snapshot(data)

    def save_user(self, data):
        self.db.insert_user(data)

    def save_snapshot(self, data):
        self.db.insert_snapshot(data)

    def run_saver(self, mq_url):
        mq = MQManager(mq_url)
        logger.info(f'creating a topic for user data')
        mq.create_user_topic()
        logger.info(f'subscribing to user topic')
        wrapped_saver_func = wrap_saver(self.db, 'user')
        thread = threading.Thread(target=mq.subscribe_to_user_topic, args=(wrapped_saver_func,))
        thread.start()
        for parser in parser_names:
            logger.info(f'creating a topic for the parsed results of {parser} parser')
            mq.create_topic(parser)
            logger.info(f'subscribing to {parser} topic')
            wrapped_saver_func = wrap_saver(self.db, 'snapshot')
            thread = threading.Thread(target=mq.subscribe_to_topic, args=(parser, wrapped_saver_func))
            thread.start()
