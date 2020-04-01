import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gzip
import struct
from final import reader_pb
from final.utils.protocol import User, Snapshot


def _read_user_data(file):
    message_size = file.read(struct.calcsize('I'))
    message_size = struct.unpack('I', message_size)[0]
    message = file.read(message_size)
    if not message:
        raise Exception("Illegal file format or problem in reading")
    return message


def get_user_info(path):
    with gzip.open(path, 'rb') as file:
        user_message = _read_user_data(file)
    user = reader_pb.User()
    user.parse_from_bytes(user_message)
    _gender = User.Gender.OTHER
    if user.gender == 0:
        _gender = User.Gender.MALE
    elif user.gender == 1:
        _gender = User.Gender.FEMALE
    return User(user.user_id, user.username, user.birthday, _gender)


def _create_protocol_snapshot_from_protobuf(snapshot):
    timestamp = snapshot.datetime
    translation = (snapshot.pose.translation.x, snapshot.pose.translation.y, snapshot.pose.translation.z)
    rotation = (snapshot.pose.rotation.x, snapshot.pose.rotation.y, snapshot.pose.rotation.z, snapshot.pose.rotation.w)
    pose = Snapshot.Pose(translation, rotation)
    color_image = Snapshot.ColorImage(snapshot.color_image.width, snapshot.color_image.height,
                                      snapshot.color_image.data)
    depth_image = Snapshot.DepthImage(snapshot.depth_image.width, snapshot.depth_image.height,
                                      snapshot.depth_image.data)
    feelings = Snapshot.Feelings(snapshot.feelings.hunger, snapshot.feelings.thirst,
                                 snapshot.feelings.exhaustion, snapshot.feelings.happiness)
    return Snapshot(timestamp, pose, color_image, depth_image, feelings)


class Reader:
    def __init__(self, path):
        self.path = path
        self.user = get_user_info(path)

    def __iter__(self):
        with gzip.open(self.path, 'rb') as file:
            _read_user_data(file)  # reading user data and ignoring it, just to advance the reader to the relevant data
            snapshot_size = file.read(struct.calcsize('I'))
            while snapshot_size:
                snapshot_size = struct.unpack('I', snapshot_size)[0]
                snapshot_message = file.read(snapshot_size)
                if not snapshot_message:
                    raise Exception("Illegal file format or problem in reading")
                snapshot = reader_pb.Snapshot()
                snapshot.parse_from_bytes(snapshot_message)
                protocol_snapshot = _create_protocol_snapshot_from_protobuf(snapshot)
                yield protocol_snapshot
                snapshot_size = file.read(struct.calcsize('I'))


reader = Reader("../sample.mind.gz")
for snapshot in reader:
    print(snapshot)
    assert 1 == 2
    break
