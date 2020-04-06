import gzip
import struct
from . import reader_pb
from .utils import protocol


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
    return protocol.init_protocol_user(user.user_id, user.username, user.birthday, user.gender)


def get_snapshot_info(snapshot_message):
    snapshot = reader_pb.Snapshot()
    snapshot.parse_from_bytes(snapshot_message)
    return protocol.init_protocol_snapshot(snapshot.datetime, snapshot.pose.translation.x,
                                           snapshot.pose.translation.y, snapshot.pose.translation.z,
                                           snapshot.pose.rotation.x, snapshot.pose.rotation.y,
                                           snapshot.pose.rotation.z, snapshot.pose.rotation.w,
                                           1, 2, 3,  # TODO
                                           1, 2, 3,  # TODO
                                           snapshot.feelings.hunger, snapshot.feelings.thirst,
                                           snapshot.feelings.exhaustion, snapshot.feelings.happiness)


class Reader:
    def __init__(self, path):
        self.path = path
        self.user = get_user_info(path)

    def __iter__(self):
        with gzip.open(self.path, 'rb') as file:
            _read_user_message(file)  # reading user data and ignoring it, to advance the reader to the relevant data
            snapshot_size = file.read(struct.calcsize('I'))
            while snapshot_size:
                snapshot_size = struct.unpack('I', snapshot_size)[0]
                snapshot_message = file.read(snapshot_size)
                if not snapshot_message:
                    raise Exception("Illegal file format or problem in reading")
                protocol_snapshot = get_snapshot_info(snapshot_message)
                yield protocol_snapshot
                snapshot_size = file.read(struct.calcsize('I'))
