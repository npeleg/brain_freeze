import requests
from ..reader import Reader
from ..utils import protocol, Logger

logger = Logger(__name__).logger


def get_parsers_from_server(host, port):
    r = requests.get(f'http://{host}:{port}/config')
    response = r.json()
    if response['error'] is not None:
        logger.error(f"could not get parsers from server due to error: {response['error']}")
        return None
    return response['parsers']


def send_to_server(host, port, user, snapshot):
    r = requests.post(f'http://{host}:{port}/snapshots', data={'user': user, 'snapshot': snapshot})
    response = r.json()
    if response['error'] is not None:
        logger.error(f"server did not accept snapshot due to error: {response['error']}")


def upload_sample(host, port, path):
    reader = Reader(path)
    user_message = protocol.init_protocol_user(reader.user.user_id, reader.user.username,
                                               reader.user.birthday, reader.user.gender)
    serialized_user_message = protocol.serialize(user_message)
    logger.info('starting to upload snapshots to server')
    for snapshot in reader:
        parsers = get_parsers_from_server(host, port)
        if parsers is None:
            continue
        config = protocol.init_protocol_config(parsers)
        partial_snapshot = protocol.build_partial_snapshot(snapshot, config)
        serialized_snapshot_message = protocol.serialize(partial_snapshot)
        send_to_server(host, port, serialized_user_message, serialized_snapshot_message)
    logger.info('finished uploading snapshots to server')
    return 0
