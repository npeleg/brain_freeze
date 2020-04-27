import pika
import sys
from ...utils import Logger

logger = Logger(__name__).logger


class RabbitMQ:
    def __init__(self, host):
        self.host = host

    def create_topic(self, topic):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        channel = connection.channel()
        logger.info(f'creating {topic} exchange')
        channel.exchange_declare(exchange=topic, exchange_type='fanout')

    def subscribe_to_topic(self, topic, func):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        channel = connection.channel()
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=topic, queue=queue_name)

        def callback(ch, method, properties, body):
            func(body)

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)

        logger.info('starting to consume from topic ' + topic)
        print('starting to consume')
        sys.stdout.flush()
        channel.start_consuming()

    def publish_to_topic(self, topic, data):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        channel = connection.channel()
        logger.info(f'sending message to topic {topic}')
        logger.debug(f'sending the message {data.__repr__}')
        channel.basic_publish(exchange=topic, routing_key='', body=data)
        connection.close()

