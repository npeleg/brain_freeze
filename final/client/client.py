from ..reader import Reader
from ..utils import Connection, protocol


def upload_sample(address, path):
    reader = Reader(path)
    for snapshot in reader:
        user_message = protocol.init_protocol_user(reader.user.user_id, reader.user.username,
                                                   reader.user.birthday, reader.user.gender)
        # TODO: are exceptions handled or should I write a handling?
        with Connection.connect(*address) as connection:
            connection.send_message(protocol.serialize(user_message))
            config = protocol.deserialize_config(connection.receive_message())
            partial_snapshot = protocol.build_partial_snapshot(snapshot, config)
            connection.send_message(protocol.serialize(partial_snapshot))
