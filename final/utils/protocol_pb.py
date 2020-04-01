from protobuf3.message import Message
from protobuf3.fields import FloatField, UInt64Field, UInt32Field, EnumField, MessageField, StringField, DoubleField, BytesField
from enum import Enum


class UserP(Message):

    class Gender(Enum):
        MALE = 0
        FEMALE = 1
        OTHER = 2


class ConfigP(Message):
    pass


class SnapshotP(Message):

    class PoseP(Message):

        class TranslationP(Message):
            pass

        class RotationP(Message):
            pass

    class ColorImageP(Message):
        pass

    class DepthImageP(Message):
        pass

    class FeelingsP(Message):
        pass

UserP.add_field('user_id', UInt64Field(field_number=1, optional=True))
UserP.add_field('username', StringField(field_number=2, optional=True))
UserP.add_field('birthday', UInt32Field(field_number=3, optional=True))
UserP.add_field('gender', EnumField(field_number=4, optional=True, enum_cls=UserP.Gender))
ConfigP.add_field('field', StringField(field_number=1, repeated=True))
SnapshotP.PoseP.TranslationP.add_field('x', DoubleField(field_number=1, optional=True))
SnapshotP.PoseP.TranslationP.add_field('y', DoubleField(field_number=2, optional=True))
SnapshotP.PoseP.TranslationP.add_field('z', DoubleField(field_number=3, optional=True))
SnapshotP.PoseP.RotationP.add_field('x', DoubleField(field_number=1, optional=True))
SnapshotP.PoseP.RotationP.add_field('y', DoubleField(field_number=2, optional=True))
SnapshotP.PoseP.RotationP.add_field('z', DoubleField(field_number=3, optional=True))
SnapshotP.PoseP.RotationP.add_field('w', DoubleField(field_number=4, optional=True))
SnapshotP.PoseP.add_field('translation', MessageField(field_number=1, optional=True, message_cls=SnapshotP.PoseP.TranslationP))
SnapshotP.PoseP.add_field('rotation', MessageField(field_number=2, optional=True, message_cls=SnapshotP.PoseP.RotationP))
SnapshotP.ColorImageP.add_field('width', UInt32Field(field_number=1, optional=True))
SnapshotP.ColorImageP.add_field('height', UInt32Field(field_number=2, optional=True))
SnapshotP.ColorImageP.add_field('data', BytesField(field_number=3, optional=True))
SnapshotP.DepthImageP.add_field('width', UInt32Field(field_number=1, optional=True))
SnapshotP.DepthImageP.add_field('height', UInt32Field(field_number=2, optional=True))
SnapshotP.DepthImageP.add_field('data', FloatField(field_number=3, repeated=True))
SnapshotP.FeelingsP.add_field('hunger', FloatField(field_number=1, optional=True))
SnapshotP.FeelingsP.add_field('thirst', FloatField(field_number=2, optional=True))
SnapshotP.FeelingsP.add_field('exhaustion', FloatField(field_number=3, optional=True))
SnapshotP.FeelingsP.add_field('happiness', FloatField(field_number=4, optional=True))
SnapshotP.add_field('datetime', UInt64Field(field_number=1, optional=True))
SnapshotP.add_field('pose', MessageField(field_number=2, optional=True, message_cls=SnapshotP.PoseP))
SnapshotP.add_field('color_image', MessageField(field_number=3, optional=True, message_cls=SnapshotP.ColorImageP))
SnapshotP.add_field('depth_image', MessageField(field_number=4, optional=True, message_cls=SnapshotP.DepthImageP))
SnapshotP.add_field('feelings', MessageField(field_number=5, optional=True, message_cls=SnapshotP.FeelingsP))
