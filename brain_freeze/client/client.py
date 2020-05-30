import requests
from ..reader import Reader
from .utils import protocol, Logger

logger = Logger(__name__).logger


def get_parsers_from_server(host, port):
    r = requests.get(f'http://{host}:{port}/config')
    response = r.json()
    if r.status_code != 200:
        logger.error(f"could not get parsers from server due to error. Got {r.status_code} status code")
        return None
    elif response['result'] != 'accepted':
        logger.error(f"could not get parsers from server due to error: {response['error']}")
        return None
    return response['parsers']


def send_to_server(host, port, data, user_id):
    if user_id is None:
        r = requests.post(f'http://{host}:{port}/users', data=data)
    else:
        r = requests.post(f'http://{host}:{port}/snapshots/{user_id}', data=data)
    response = r.json()
    if r.status_code != 201:
        logger.error(f"server did not accept data due to error. Got {r.status_code} status code")
        return False
    if response['result'] != 'accepted':
        logger.error(f"error: {response['error']}")
        return False
    return True


def upload_sample(host, port, path):
    sent_successfully = True
    reader = Reader(path)

    logger.info('uploading user information')
    user_message = protocol.init_protocol_user(reader.user.user_id, reader.user.username,
                                               reader.user.birthday, reader.user.gender)
    serialized_user_message = protocol.serialize(user_message)
    sent = send_to_server(host, port, serialized_user_message, None)
    if not sent:
        sent_successfully = False

    logger.info('uploading snapshots to server')
    print('uploading...')
    count = 0
    for snapshot in reader:
        count += 1
        parsers = get_parsers_from_server(host, port)
        if not parsers:
            logger.info("no parsers supported in this server")
            continue
        config = protocol.init_protocol_config(parsers)
        partial_snapshot = protocol.build_partial_snapshot(snapshot, config)
        serialized_snapshot_message = protocol.serialize(partial_snapshot)
        sent = send_to_server(host, port, serialized_snapshot_message, user_message.user_id)
        if not sent:
            logger.debug(f'snapshot {count} upload failed')
            sent_successfully = False
        else:
            logger.debug(f'snapshot {count} uploaded successfully')
    logger.info('finished uploading snapshots to server')

    if not sent_successfully:
        return 1
    return 0

# with open('./image_bytes', 'wb') as file:
#    file.write(snapshot.color_image.data)
#    logger.info('saved')
