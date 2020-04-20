import pika


class RabbitMQ:
    def __init__(self, host):
        self.host = host
        self.exchanges = []

    def create_topic(self, topic):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        channel = connection.channel()
        channel.exchange_declare(exchange=topic, exchange_type='fanout')
        self.exchanges.append(topic)

    def subscribe_to_topic(self, topic, func):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        channel = connection.channel()
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=topic, queue=queue_name)

        def callback(ch, method, properties, body):
            res = func(body)
            if res is not None:
                self.publish_to_topic(topic, res)

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)

        channel.start_consuming()

    def publish_to_topic(self, topic, data):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        channel = connection.channel()
        channel.basic_publish(exchange=topic, routing_key='', body=data)
        # Todo logging(" [x] Sent %r" % message)
        connection.close()

    def publish_to_all_topics(self, data):
        for exchange in self.exchanges:
            self.publish_to_topic(exchange, data)
