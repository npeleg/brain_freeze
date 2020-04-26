from .logger import Logger
from .rabbit_mq import RabbitMQ
from .service_finder import find_service

logger = Logger(__name__).logger
mqs = {"rabbitmq": RabbitMQ}


class MQManager:
    def __init__(self, url):
        self.mq = find_service(url, mqs)

    def create_topic(self, topic):
        self.mq.create_topic(topic)

    def create_incoming_topic(self):
        self.create_topic('incoming')

    def subscribe_to_topic(self, topic, func):
        self.mq.subscribe_to_topic(topic, func)

    def subscribe_to_incoming_topic(self, func):
        self.create_incoming_topic()
        self.subscribe_to_topic('incoming', func)

    def publish_to_topic(self, topic, data):
        if data is not None:
            self.mq.publish_to_topic(topic, data)

    def publish_to_incoming_topic(self, data):
        self.publish_to_topic('incoming', data)
