from .rabbit_mq import RabbitMQ
from ..parsers import Parsers
from ..utils import Logger, find_service

logger = Logger(__name__).logger
mqs = {"rabbitmq": RabbitMQ}


class MQManager:
    def __init__(self, url):
        self.mq = find_service(url, mqs)
        # creating a topic for incoming messages
        self.mq.create_topic('incoming')
        self.parsers = Parsers().parsers_dict
        for parser_name, parser in self.parsers.items():
            logger.info(f'subscribing {parser_name} parser to incoming topic and adding a topic for its parsed results')
            self.mq.subscribe_to_topic('incoming', parser)
            self.mq.create_topic(parser_name)

    def send(self, data):
        if data is not None:
            self.mq.publish_to_topic('incoming', data)
