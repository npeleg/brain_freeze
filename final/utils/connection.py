import socket
import struct


class Connection:
    def __init__(self, socket):
        self.socket = socket

    def __repr__(self):
        return f"<Connection from {str(self.socket.getsockname()[0])}:{str(self.socket.getsockname()[1])} to {str(self.socket.getpeername()[0])}:{str(self.socket.getpeername()[1])}>"

    def send_message(self, data):
        data_length = struct.pack('I', struct.calcsize(data))
        self.socket.sendall(data_length + data)

    def receive_message(self):
        msg = bytes()
        msg_length = bytes()

        # receiving the length of the message:
        while self.socket and len(msg_length) < struct.calcsize('I'):
            received = self.socket.recv(struct.calcsize('I') - len(msg_length))
            if not received:
                raise Exception("Connection closed before all data received")
            msg_length += received
        if len(msg_length) < struct.calcsize('I'):
            raise Exception("Connection closed before all data received")
        msg_length = struct.unpack('I', msg_length)[0]

        # receiving the message:
        while self.socket and len(msg) < msg_length:
            received = self.socket.recv(msg_length - len(msg))
            if not received:
                raise Exception("Connection closed before all data received")
            msg += received
        if len(msg) < msg_length:
            raise Exception("Connection closed before all data received")
        return msg

    def close(self):
        self.socket.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @classmethod
    def connect(cls, host, port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        return Connection(client_socket)
