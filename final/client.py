from .reader import Reader
from .utils import Connection, protocol


def upload_sample(address):
    reader = Reader('../sample.mind.gz')
    for snapshot in reader:
        user_message = protocol.User(reader.user.user_id, reader.user.username,
                                     reader.user.birthday, reader.user.gender)
        # TODO: are exceptions handled or should I write a handling?
        with Connection.connect(*address) as connection:
            connection.send_message(user_message.serialize())
            config = protocol.Config.deserialize(connection.receive_message())
            partial_snapshot = snapshot.build_partial_snapshot(config)
            connection.send_message(partial_snapshot.serialize())
