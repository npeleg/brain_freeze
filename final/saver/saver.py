from ..utils import find_service

dbs = {}


class Saver:
    def __init__(self, url):
        self.db = find_service(url, dbs)

    def save(self, parser_name, data):
        if data is not None:
            pass
            # TODO save data to self.db
