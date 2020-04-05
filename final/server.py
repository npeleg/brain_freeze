import importlib
import os
import pathlib
import sys
import time
import threading
from .utils import Listener, protocol


class ClientThread(threading.Thread):
    lock = threading.Lock()

    def __init__(self, client_connection, data_dir):
        threading.Thread.__init__(self)
        self.client_socket = client_connection
        self.data_dir = pathlib.Path(data_dir)

    def run(self):  # TODO edit
        # parsers = Parsers()
        # parsers.load_parsers('./parsers')

        # receiving 'user' message from client:
        user = protocol.User.deserialize(self.client_socket.receive_message())

        # sending 'config' message to client:
        # config = protocol.Config(parsers.get_fields())
        config = protocol.Config({'translation', 'rotation'})
        self.client_socket.send_message(config.serialize())

        # receiving 'snapshot' message from client:
        snapshot = protocol.Snapshot.deserialize((self.client_socket.receive_message()))

        timestamp = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(snapshot.datetime / 1000))
        path = self.data_dir / str(user.user_id) / str(timestamp)
        context = Context(path)

        ClientThread.lock.acquire()
        # parsers.parse_fields(context, snapshot)
        context.save("translation.txt", snapshot.__repr__())
        ClientThread.lock.release()


def run_server(address, data_dir):
    with Listener(port=address[1], host=address[0]) as listener:
        while True:
            client_connection = listener.accept()
            print("accepted ")
            new_thread = ClientThread(client_connection, data_dir)
            new_thread.start()


class Parsers:
    def __init__(self):
        self.supported_fields = {}

    def get_fields(self):  # TODO re-implement according to load_parsers
        return self.supported_fields.keys()

    @classmethod
    def load_parsers(cls, parsers_dir):
        parsers_dir = pathlib.Path(parsers_dir).absolute()
        sys.path.insert(0, str(parsers_dir.parent))
        for path in parsers_dir.iterdir():
            if path.name.startswith('_') or not path.suffix == ".py":
                continue
            importlib.import_module(f'{parsers_dir.name}.{path.stem}', package=parsers_dir.name)

    def parse_fields(self, context, snapshot):
        for field in self.supported_fields:
            self.supported_fields[field](context, snapshot)


class Context:
    def __init__(self, dir):
        self.dir = dir

    def save(self, filename, contents):
        pathlib.Path(self.dir).mkdir(parents=True, exist_ok=True)
        with open(self.dir / filename, 'w') as file:
            file.write(contents)
