from brain_freeze.reader import Reader
from brain_freeze.utils import protocol


def test_serialize_deserialize():
    reader = Reader('./tests/utils/small_sample.mind.gz')
    assert reader.user.__repr__() == protocol.deserialize_user(protocol.serialize(reader.user)).__repr__()
    for snapshot in reader:
        assert snapshot.__repr__() == protocol.deserialize_snapshot(protocol.serialize(snapshot)).__repr__()
        break

