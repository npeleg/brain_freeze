from .logger import Logger
from .rabbitmq import RabbitMQ
from .service_finder import find_service

logger = Logger(__name__).logger
mqs = {"rabbitmq": RabbitMQ}
USER_TOPIC = 'users'
SNAPSHOT_TOPIC = 'snapshots'


class MQManager:
    def __init__(self, url):
        self.mq = find_service(url, mqs)

    def create_topic(self, topic):
        self.mq.create_topic(topic)

    def create_snapshot_topic(self):
        self.create_topic(SNAPSHOT_TOPIC)

    def create_user_topic(self):
        self.create_topic(USER_TOPIC)

    def subscribe_to_topic(self, topic, func):
        self.mq.subscribe_to_topic(topic, func)

    def subscribe_to_snapshot_topic(self, func):
        self.subscribe_to_topic(SNAPSHOT_TOPIC, func)

    def subscribe_to_user_topic(self, func):
        self.subscribe_to_topic(USER_TOPIC, func)

    def publish_to_topic(self, topic, data):
        if data is None:
            return
        self.mq.publish_to_topic(topic, data)

    def publish_to_snapshot_topic(self, data):
        self.publish_to_topic(SNAPSHOT_TOPIC, data)

    def publish_to_user_topic(self, data):
        self.publish_to_topic(USER_TOPIC, data)
