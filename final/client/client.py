from ..reader import Reader
from ..utils import Connection, protocol, Logger

logger = Logger(__name__).logger


def upload_sample(address, path):
    reader = Reader(path)
    user_message = protocol.init_protocol_user(reader.user.user_id, reader.user.username,
                                               reader.user.birthday, reader.user.gender)
    serialized_user_message = protocol.serialize(user_message)
    logger.info('starting to upload snapshots to server')
    for snapshot in reader:
        with Connection.connect(*address) as connection:
            connection.send_message(serialized_user_message)
            config = protocol.deserialize_config(connection.receive_message())
            partial_snapshot = protocol.build_partial_snapshot(snapshot, config)
            connection.send_message(protocol.serialize(partial_snapshot))
    logger.info('finished uploading snapshots to server')
    return 0
