from ..utils import find_service, Logger, MQManager

logger = Logger(__name__).logger
dbs = {}
parsers = {'pose'}


def func(data):
    logger.info("called from saver")
    logger.info(data)
    print("OK")


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
        mq.subscribe_to_topic('pose', func)
