from .reader import Reader
from .utils import Connection, protocol


def upload_sample(address):
    reader = Reader('../sample.mind.gz')
    for snapshot in reader:
        hello_message = protocol.User(reader.user_id, reader.username, reader.birthday, reader.gender)
        with Connection.connect(*address) as connection:  # TODO: are exceptions handled or should I write a handling?
            connection.send_message(hello_message.serialize())                  # sending 'hello' message to server
            config = protocol.Config.deserialize(connection.receive_message())  # receiving 'config' message from server
            partial_snapshot = snapshot.build_partial_snapshot(config)
            connection.send_message(partial_snapshot.serialize())
