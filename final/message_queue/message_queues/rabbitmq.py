from furl import furl as f


class RabbitMQ:
    def __init__(self, url):
        parsed_url = f(url)
        self.host = parsed_url.host
        self.port = parsed_url.port

    def publish(self, data):
        pass

    def subscribe(self):
        pass
