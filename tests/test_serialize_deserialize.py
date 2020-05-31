from brain_freeze.reader import Reader
from brain_freeze.utils import protocol


def test_serialize_deserialize():
    reader = Reader('./tests/utils/small_sample.mind.gz')
    serialized = protocol.serialize(reader.user)
    assert reader.user.__repr__() == \
           protocol.deserialize_user(serialized).__repr__()
    for snapshot in reader:
        serialized = protocol.serialize(snapshot)
        assert snapshot.__repr__() == \
               protocol.deserialize_snapshot(serialized).__repr__()
        break
