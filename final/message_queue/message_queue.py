from datetime import datetime as dt
from .message_queues.rabbitmq import RabbitMQ

mqs = {"rabbitmq" : RabbitMQ}


def find_mq(url):
    for scheme, cls in mqs.items():
        if url.startswith(scheme):
            return cls(url)
    raise ValueError(f'invalid url: {url}')


class MessageQueue:
    def __init__(self, url):
        self.mq = find_mq(url)
        self.parsers =
        # parsers = Parsers()
        # parsers.load_parsers('./parsers')
        # config = protocol.Config(parsers.get_fields())
        timestamp = dt.fromtimestamp(snapshot.datetime / 1000)
        timestamp = timestamp.strftime('%Y-%m-%d_%H-%M-%S.%f')[:-3]
        context = Context(path)

        # parsers.parse_fields(context, snapshot)
        context.save("translation.txt", protocol.repr_protocol_snapshot(snapshot))

    def send(self, data):
        if data is not None:
            self.mq.publish(data)
