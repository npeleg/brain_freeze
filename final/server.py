import importlib
import pathlib
import time
import threading
import sys
from .utils import Listener, protocol


class ClientThread(threading.Thread):
    lock = threading.Lock()

    def __init__(self, client_connection, data_dir):
        threading.Thread.__init__(self)
        self.client_socket = client_connection
        self.data_dir = data_dir

    def run(self):
        parsers = Parsers()
        parsers.load_parsers('./parsers')

        # receiving 'hello' message from client:
        hello = protocol.Hello.deserialize(self.client_socket.receive_message())
        path = pathlib.Path(f"{self.data_dir}/{hello.user_id}")

        # sending 'config' message to client:
        config = protocol.Config(parsers.get_fields())
        self.client_socket.send_message(config.serialize())

        # receiving 'snapshot' message from client:
        snapshot = protocol.Snapshot.deserialize((self.client_socket.receive_message()))

        date_time = time.strftime('%Y-%m-%d_%H-%M-%S-%f', time.localtime(snapshot.timestamp))
        path = pathlib.Path(str(path) + "/" + date_time)
        context = Context(path)

        ClientThread.lock.acquire()
        parsers.parse_fields(context, snapshot)
        ClientThread.lock.release()


def run_server(address, data_dir):
    pathlib.Path(data_dir).mkdir(parents=True, exist_ok=True)
    with Listener(port=address[1], host=address[0]) as listener:
        client_connection = listener.accept()
        new_thread = ClientThread(client_connection, data_dir)
        new_thread.start()


class Parsers:
    def __init__(self):
        self.supported_fields = {}

    def get_fields(self):  # TODO re-implement according to load_parsers
        return self.supported_fields.keys()

    def load_parsers(self, parsers_dir):
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
    def __init__(self, directory):
        self.directory = directory

    def save(self, filename, contents):
        with open(self.directory / filename) as file:
            file.write(contents)
