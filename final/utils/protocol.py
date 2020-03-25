import enum
import time
from . import protocol_layer_pb2


class User:
    class Gender(enum.Enum):
        MALE = 0
        FEMALE = 1
        OTHER = 2

    def __init__(self, user_id, username, birthday, gender):
        self.user_id = user_id
        self.username = username
        self.birthday = birthday
        _gender = 'OTHER'
        if gender == 0:
            _gender = 'MALE'
        elif gender == 1:
            _gender = 'FEMALE'
        self.gender = User.Gender[_gender]

    def __repr__(self):
        dt = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(self.birthday))
        return f'user {self.user_id}: {self.username}, born {self.birthday} ({self.gender.name})'

    def serialize(self):
        user_message = protocol_layer_pb2.UserP()
        user_message.user_id = self.user_id
        user_message.username = self.username
        user_message.birthday = self.birthday
        user_message.gender = self.gender
        return user_message.SerializeToString()

    @classmethod
    def deserialize(cls, data):
        user = protocol_layer_pb2.UserP()
        user.ParseFromString(data)
        user_id = user.user_id
        username = user.username
        birthday = user.birthday
        gender = user.gender
        return User(user_id, username, birthday, gender)


class Config:
    def __init__(self, supported_fields):
        self.supported_fields = supported_fields

    def serialize(self):
        config_message = protocol_layer_pb2.ConfigP()
        for field in self.supported_fields:
            to_add = config_message.supported_fields.add()
            to_add = field
        return config_message.SerializeToString()

    @classmethod
    def deserialize(cls, data):
        supported_fields = []
        config = protocol_layer_pb2.ConfigP()
        config.ParseFromString(data)
        for field in config.supported_fields:
            supported_fields.append(field)
        return Config(supported_fields)


class Snapshot:
    def __init__(self, datetime, pose, color_image, depth_image, feelings):
        self.datetime = datetime  # TODO need to convert from milliseconds to seconds
        self.pose = pose
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings

    class Pose:
        def __init__(self, translation, rotation):
            self.translation = translation
            self.rotation = rotation

    class ColorImage:
        def __init__(self, width, height, pixels):
            self.width = width
            self.height = height
            self.pixels = pixels

    class DepthImage:
        def __init__(self, width, height, pixels):
            self.width = width
            self.height = height
            self.pixels = pixels

    class Feelings:
        def __init__(self, hunger, thirst, exhaustion, happiness):
            self.hunger = hunger
            self.thirst = thirst
            self.exhaustion = exhaustion
            self.happiness = happiness

    def __repr__(self):
        dt = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(self.datetime))
        return f'{dt}: Pose is {self.pose.translation}, {self.pose.rotation}\n \
              Color Image dimensions: {self.color_image.width}X{self.color_image.height}\n \
              Depth Image dimensions: {self.depth_image.width}X{self.depth_image.height}\n \
              Hunger: {self.feelings.hunger}, Thirst: {self.feelings.thirst}, Exhaustion: {self.feelings.exhaustion} \
              Happiness: {self.feelings.happiness}'

    def serialize(self):
        snapshot_message = protocol_layer_pb2.SnapshotP()
        snapshot_message.datetime = self.datetime

        snapshot_message.PoseP.TranslationP.x = self.pose.translation[0]
        snapshot_message.PoseP.TranslationP.y = self.pose.translation[1]
        snapshot_message.PoseP.TranslationP.z = self.pose.translation[2]
        snapshot_message.PoseP.RotationP.x = self.pose.rotation[0]
        snapshot_message.PoseP.RotationP.y = self.pose.rotation[1]
        snapshot_message.PoseP.RotationP.z = self.pose.rotation[2]
        snapshot_message.PoseP.RotationP.w = self.pose.rotation[3]

        snapshot_message.ColorImageP.width = self.color_image.width
        snapshot_message.ColorImageP.height = self.color_image.height
        snapshot_message.ColorImageP.data = self.color_image.pixels

        snapshot_message.DepthImageP.width = self.depth_image.width
        snapshot_message.DepthImageP.height = self.depth_image.height
        snapshot_message.DepthImageP.data = self.depth_image.pixels

        snapshot_message.FeelingsP.hunger = self.feelings.hunger
        snapshot_message.FeelingsP.thirst = self.feelings.thirst
        snapshot_message.FeelingsP.exhaustion = self.feelings.exhaustion
        snapshot_message.FeelingsP.happiness = self.feelings.happiness

        return snapshot_message.SerializeToString()

    @classmethod
    def deserialize(cls, data):
        snapshot_message = protocol_layer_pb2.SnapshotP()
        snapshot_message.ParseFromString(data)

        datetime = snapshot_message.datetime

        translation = (snapshot_message.PoseP.TranslationP.x, snapshot_message.PoseP.TranslationP.y,
                       snapshot_message.PoseP.TranslationP.z)
        rotation = (snapshot_message.PoseP.RotationP.x, snapshot_message.PoseP.RotationP.y,
                    snapshot_message.PoseP.RotationP.z, snapshot_message.PoseP.RotationP.w)

        color_width = snapshot_message.ColorImageP.width
        color_height = snapshot_message.ColorImageP.height
        color_pixels = snapshot_message.ColorImageP.pixels

        depth_width = snapshot_message.DepthImageP.width
        depth_height = snapshot_message.DepthImageP.height
        depth_pixels = snapshot_message.DepthImageP.pixels

        hunger = snapshot_message.FeelingsP.hunger
        thirst = snapshot_message.FeelingsP.thirst
        exhaustion = snapshot_message.FeelingsP.exhaustion
        happiness = snapshot_message.FeelingsP.happiness

        return Snapshot(datetime, Snapshot.Pose(translation, rotation),
                        Snapshot.ColorImage(color_width, color_height, color_pixels),
                        Snapshot.DepthImage(depth_width, depth_height, depth_pixels),
                        Snapshot.Feelings(hunger, thirst, exhaustion, happiness))

    def build_partial_snapshot(self, config):
        """builds a new snapshot according to config"""
        translation = self.pose.translation if 'translation' in config.supported_fields else (0, 0, 0)
        rotation = self.pose.rotation if 'rotation' in config.supported_fields else (0, 0, 0, 0)
        color_width = self.color_image.width if 'color_image' in config.supported_fields else 0
        color_height = self.color_image.height if 'color_image' in config.supported_fields else 0
        color_pixels = self.color_image.pixels if 'color_image' in config.supported_fields else None
        depth_width = self.depth_image.width if 'depth_image' in config.supported_fields else 0
        depth_height = self.depth_image.height if 'depth_image' in config.supported_fields else 0
        depth_pixels = self.color_image.pixels if 'depth_image' in config.supported_fields else None
        feelings = self.feelings if 'feelings' in config.supported_fields else (0, 0, 0, 0)

        return Snapshot(self.datetime, Snapshot.Pose(translation, rotation),
                        Snapshot.ColorImage(color_width, color_height, color_pixels),
                        Snapshot.DepthImage(depth_width, depth_height, depth_pixels), Snapshot.Feelings(*feelings))
