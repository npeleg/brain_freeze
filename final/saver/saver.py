import threading
from ..utils import find_service, Logger, MQManager

logger = Logger(__name__).logger
dbs = {}
parsers = {'pose', 'feelings'}
lock = threading.Lock()


def func(data):
    with lock:
        logger.info("received data from exchange")
        logger.info(data)


class Saver:
    def __init__(self, url):
        pass
        # self.db = find_service(url, dbs)

    def save(self, parser_name, data):
        if data is None:
            return
        # TODO save data to self.db

    def run_saver(self, mq_url):
        # TODO how to make this work with all the parsers
        mq = MQManager(mq_url)
        logger.info(f'creating a topic for user data')
        mq.create_user_topic()
        logger.info(f'subscribing to user topic')
        thread = threading.Thread(target=mq.subscribe_to_user_topic, args=(func,))
        thread.start()
        for parser in parsers:
            logger.info(f'creating a topic for the parsed results of {parser} parser')
            mq.create_topic(parser)
            logger.info(f'subscribing to {parser} topic')
            thread = threading.Thread(target=mq.subscribe_to_topic, args=(parser, func))
            thread.start()
