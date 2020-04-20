from furl import furl as f
from .message_queues import RabbitMQ
from ..parsers import Parsers

mqs = {"rabbitmq": RabbitMQ}


def find_mq(url):
    parsed_url = f(url)
    for scheme, cls in mqs.items():
        if parsed_url.scheme.startswith(scheme):
            return cls(parsed_url.host)
    raise ValueError(f'invalid url: {url}')


class MQManager:
    def __init__(self, url):
        self.mq = find_mq(url)
        self.parsers = Parsers().parsers_dict
        for name, parser in self.parsers.items():
            self.mq.create_topic(name)
            self.mq.subscribe_to_topic(name, parser)

    def send(self, data):
        if data is not None:
            self.mq.publish_to_all_topics(data)
