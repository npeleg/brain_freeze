import gzip
import struct
from . import reader_pb2
from .utils.protocol import User, Snapshot


def _read_user_data(file):
    message_size = file.read(struct.calcsize('I'))
    message_size = struct.unpack('I', message_size)[0]
    return file.read(message_size)


def _create_protocol_snapshot_from_protobuf(snapshot):
    timestamp = snapshot.datetime / 1000
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
        with gzip.open(path, 'rb') as file:
            user_message = _read_user_data(file)
        user = reader_pb2.User()
        user.ParseFromString(user_message)
        self.user = User(user.user_id, user.username, user.birthday / 1000, user.gender)

    def __iter__(self):
        count = 0
        with gzip.open(self.path, 'rb') as file:
            _read_user_data(file)  # reading user data and ignoring it, just to advance the reader to the relevant data
            snapshot_size = file.read(struct.calcsize('I'))
            while snapshot_size:
                snapshot_size = struct.unpack('I', snapshot_size)[0]
                snapshot_message = file.read(snapshot_size)
                if not snapshot_message:
                    raise Exception("Illegal file format or problem in reading")
                snapshot = reader_pb2.Snapshot()
                snapshot.ParseFromString(snapshot_message)
                protocol_snapshot = _create_protocol_snapshot_from_protobuf(snapshot)
                count += 1
                yield protocol_snapshot
                snapshot_size = file.read(struct.calcsize('I'))
