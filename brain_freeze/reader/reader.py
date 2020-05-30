import gzip
import struct
from . import reader_pb
from ..utils import protocol, protocol_pb, Logger

logger = Logger(__name__).logger


def get_protocol_gender(gender):
    _gender = protocol_pb.UserP.Gender.OTHER
    if gender == reader_pb.User.Gender.MALE:
        _gender = protocol_pb.UserP.Gender.MALE
    elif gender == reader_pb.User.Gender.FEMALE:
        _gender = protocol_pb.UserP.Gender.FEMALE
    return _gender


def _read_user_message(file):
    message_size = file.read(struct.calcsize('I'))
    message_size = struct.unpack('I', message_size)[0]
    message = file.read(message_size)
    if not message:
        raise Exception("Illegal file format or problem in reading")
    return message


def get_user_info(path):
    with gzip.open(path, 'rb') as file:
        user_message = _read_user_message(file)
    user = reader_pb.User()
    user.parse_from_bytes(user_message)
    return protocol.init_protocol_user(user.user_id, user.username, user.birthday, get_protocol_gender(user.gender))


def parse_snapshot(snapshot_message):
    snapshot = reader_pb.Snapshot()
    snapshot.parse_from_bytes(snapshot_message)
    try:
        protocol_snapshot = protocol.init_protocol_snapshot(snapshot.datetime, snapshot.pose.translation.x,
                                    snapshot.pose.translation.y, snapshot.pose.translation.z,
                                    snapshot.pose.rotation.x, snapshot.pose.rotation.y,
                                    snapshot.pose.rotation.z, snapshot.pose.rotation.w,
                                    snapshot.color_image.width, snapshot.color_image.width, snapshot.color_image.data,
                                    1, 2, 3,  # TODO
                                    snapshot.feelings.hunger, snapshot.feelings.thirst,
                                    snapshot.feelings.exhaustion, snapshot.feelings.happiness)
    except Exception as error:
        logger.error(error)
    logger.info('returning snapshot')
    return protocol_snapshot


class Reader:
    def __init__(self, path):
        self.path = path
        self.user = get_user_info(path)

    def __iter__(self):
        with gzip.open(self.path, 'rb') as file:
            # reading user data and ignoring it, to advance the reader to the relevant data
            _read_user_message(file)
            snapshot_size = file.read(struct.calcsize('I'))
            while snapshot_size:
                snapshot_size = struct.unpack('I', snapshot_size)[0]
                snapshot_bytes = file.read(snapshot_size)
                if not snapshot_bytes:
                    raise Exception("Illegal file format or problem in reading")
                logger.info('sending to parse_snapshot')
                snapshot = parse_snapshot(snapshot_bytes)
                logger.info('yielding snapshot')
                yield snapshot
                snapshot_size = file.read(struct.calcsize('I'))
                