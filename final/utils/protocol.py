from datetime import datetime as dt
from final.utils import protocol_pb


def serialize(message):
    return message.encode_to_bytes()


# User Functions:
def get_gender(gender):
    _gender = protocol_pb.UserP.Gender.OTHER
    if gender == 0:
        _gender = protocol_pb.UserP.Gender.MALE
    elif gender == 1:
        _gender = protocol_pb.UserP.Gender.FEMALE
    return _gender


def init_protocol_user(user_id, username, birthday, gender):
    user = protocol_pb.UserP()
    user.user_id = user_id
    user.username = username
    user.birthday = birthday
    user.gender = get_gender(gender)
    return user


def repr_protocol_user(user):
    birthday = dt.fromtimestamp(user.birthday / 1000)
    birthday = birthday.strftime('%Y-%m-%d')
    return f'user {user.user_id}: {user.username}, born {birthday} ({user.gender.name})'


def deserialize_user(data):
    user = protocol_pb.UserP()
    user.parse_from_bytes(data)
    return user


# Config Functions:
def init_protocol_config(supported_fields):
    config = protocol_pb.ConfigP()
    for field in supported_fields:
        config.supported_fields.append(field)
    return config


def deserialize_config(data):
    config = protocol_pb.ConfigP()
    config.parse_from_bytes(data)
    return config


# Snapshot Functions:
def init_protocol_snapshot(datetime, t_x, t_y, t_z, r_x, r_y, r_z, r_w,
                           color_width, color_height, color_data,
                           depth_width, depth_height, depth_data,
                           hunger, thirst, exhaustion, happiness):
    snapshot = protocol_pb.SnapshotP()
    snapshot.datetime = datetime
    snapshot.pose.translation.x = t_x
    snapshot.pose.translation.y = t_y
    snapshot.pose.translation.z = t_z
    snapshot.pose.rotation.x = r_x
    snapshot.pose.rotation.y = r_y
    snapshot.pose.rotation.z = r_z
    snapshot.pose.rotation.w = r_w
    snapshot.color_image.width = color_width
    snapshot.color_image.height = color_height
    # snapshot.color_image.data = color_data TODO
    snapshot.depth_image.width = depth_width
    snapshot.depth_image.height = depth_height
    # snapshot.depth_image.data = depth_data TODO
    snapshot.feelings.hunger = hunger
    snapshot.feelings.thirst = thirst
    snapshot.feelings.exhaustion = exhaustion
    snapshot.feelings.happiness = happiness
    return snapshot


def repr_protocol_snapshot(snapshot):
    timestamp = dt.fromtimestamp(snapshot.datetime / 1000)
    timestamp = timestamp.strftime('%Y-%m-%d_%H-%M-%S.%f')[:-3]
    return f'{timestamp}:\n' \
           f'Translation is ({snapshot.pose.translation.x}, {snapshot.pose.translation.y}, ' \
           f'{snapshot.pose.translation.z})\n' \
           f'Rotation is ({snapshot.pose.rotation.x}, {snapshot.pose.rotation.y}, ' \
           f'{snapshot.pose.rotation.z}, {snapshot.pose.rotation.w})\n' \
           f'Color Image dimensions: {snapshot.color_image.width}X{snapshot.color_image.height}\n' \
           f'Depth Image dimensions: {snapshot.depth_image.width}X{snapshot.depth_image.height}\n' \
           f'Hunger: {snapshot.feelings.hunger}, Thirst: {snapshot.feelings.thirst}, ' \
           f'Exhaustion: {snapshot.feelings.exhaustion}, Happiness: {snapshot.feelings.happiness}\n'


def deserialize_snapshot(data):
    snapshot = protocol_pb.SnapshotP()
    snapshot.parse_from_bytes(data)
    return snapshot


def build_partial_snapshot(snapshot, config):
    """builds a new snapshot according to config"""
    if 'pose' in config.supported_fields:
        t_x, t_y, t_z = snapshot.pose.translation.x, snapshot.pose.translation.y, \
                        snapshot.pose.translation.z
        r_x, r_y, r_z, r_w = snapshot.pose.rotation.x, snapshot.pose.rotation.y, \
                             snapshot.pose.rotation.z, snapshot.pose.rotation.w
    else:
        t_x = t_y = t_z = r_x = r_y = r_z = r_w = 0

    if 'color_image' in config.supported_fields:
        color_width, color_height, color_data = snapshot.color_image.width, snapshot.color_image.height, \
                                                snapshot.color_image.data
    else:
        color_width, color_height, color_data = 0, 0, None

    if 'depth_image' in config.supported_fields:
        depth_width, depth_height, depth_data = snapshot.depth_image.width, snapshot.depth_image.height, \
                                                snapshot.depth_image.data
    else:
        depth_width, depth_height, depth_data = 0, 0, None

    if 'feelings' in config.supported_fields:
        hunger, thirst, exhaustion, happiness = snapshot.feelings.hunger, snapshot.feeling.thirst, \
                                                snapshot.feelings.exhaustion, snapshot.feelings.happiness
    else:
        hunger = thirst = exhaustion = happiness = 0

    return init_protocol_snapshot(snapshot.datetime, t_x, t_y, t_z, r_x, r_y, r_z, r_w,
                                  color_width, color_height, color_data,
                                  depth_width, depth_height, depth_data,
                                  hunger, thirst, exhaustion, happiness)
