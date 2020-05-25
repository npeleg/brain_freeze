import sys
import threading
from ..utils import Logger, MQManager, DBManager

logger = Logger(__name__).logger
parser_names = {'pose', 'feelings'}
lock = threading.Lock()


def wrap_saver(db, content):
    """ returns a function that saves data to the relevant table in the db """
    def save_user_to_db(data):
        with lock:
            logger.info('sending user data to save in db')
        db.insert_user(data)

    def save_snapshot_to_db(data):
        with lock:
            logger.info('sending snapshot data to save in db')
        db.insert_snapshot('', data)

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
        return self.db.insert_snapshot(parser_name, data)

    def run_saver(self, mq_url):
        mq = MQManager(mq_url)
        for parser in parser_names:
            logger.info(f'creating a topic for the parsed results of {parser} parser')
            mq.create_topic(parser)
            logger.info(f'subscribing to {parser} topic')
            wrapped_saver_func = wrap_saver(self.db, 'snapshot')
            thread = threading.Thread(target=mq.subscribe_to_topic, args=(parser, wrapped_saver_func))
            thread.start()
        logger.info(f'creating a topic for user data')
        mq.create_user_topic()
        logger.info(f'subscribing to user topic')
        wrapped_saver_func = wrap_saver(self.db, 'user')
        print('running...')
        sys.stdout.flush()
        mq.subscribe_to_user_topic(wrapped_saver_func)


