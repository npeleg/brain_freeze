from . import Connection
import socket


class Listener:
    def __init__(self, port, host="0.0.0.0", backlog=1000, reuseaddr=True):
        self.port = int(port)
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        self.socket = None

    def __repr__(self):
        return f"Listener(port={str(self.port)}, host='{self.host}'," \
               f"backlog={str(self.backlog)}, reuseaddr={str(self.reuseaddr)})"

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.reuseaddr:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.backlog)

    def stop(self):
        self.socket.close()

    def accept(self):
        client_socket, _ = self.socket.accept()
        return Connection(client_socket)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
