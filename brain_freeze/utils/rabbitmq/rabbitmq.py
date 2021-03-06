import pika
from ..logger import Logger

logger = Logger(__name__).logger


class RabbitMQ:
    def __init__(self, host, port):
        self.host = host

    def create_topic(self, topic):
        host = self.host
        connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        channel = connection.channel()
        logger.info(f'creating {topic} exchange')
        channel.exchange_declare(exchange=topic, exchange_type='fanout')

    def subscribe_to_topic(self, topic, func):
        host = self.host
        connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        channel = connection.channel()
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=topic, queue=queue_name)

        def callback(ch, method, properties, body):
            logger.info(f'callback function {func.__name__} called')
            logger.debug('callback function called on data ' + body.__repr__())
            func(body)

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)

        logger.info(f'starting to consume from {topic} exchange ')
        channel.start_consuming()

    def publish_to_topic(self, topic, data):
        host = self.host
        connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        channel = connection.channel()
        logger.info(f'sending message to {topic} exchange')
        logger.debug(f'sending the message {data.__repr__}')
        channel.basic_publish(exchange=topic, routing_key='', body=data)
        connection.close()
