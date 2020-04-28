from .logger import Logger
from .rabbit_mq import RabbitMQ
from .service_finder import find_service

logger = Logger(__name__).logger
mqs = {"rabbitmq": RabbitMQ}
INCOMING = 'incoming'


class MQManager:
    def __init__(self, url):
        self.mq = find_service(url, mqs)
        self.topics = []

    def create_topic(self, topic):
        self.mq.create_topic(topic)
        self.topics.append(topic)

    def create_incoming_topic(self):
        self.create_topic(INCOMING)

    def subscribe_to_topic(self, topic, func):
        self.mq.subscribe_to_topic(topic, func)

    def subscribe_to_incoming_topic(self, func):
        if INCOMING not in self.topics:
            self.create_incoming_topic()
        self.subscribe_to_topic(INCOMING, func)

    def publish_to_topic(self, topic, data):
        if data is None:
            return
        self.mq.publish_to_topic(topic, data)

    def publish_to_incoming_topic(self, data):
        if INCOMING not in self.topics:
            self.create_incoming_topic()
        self.publish_to_topic(INCOMING, data)
