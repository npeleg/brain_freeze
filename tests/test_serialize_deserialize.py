from final import Reader
from final.utils import protocol


def test_serialize_deserialize():
    reader = Reader('./tests/utils/small_sample.mind.gz')
    assert reader.user.__repr__() == protocol.User.deserialize(reader.user.serialize()).__repr__()
    for snapshot in reader:
        print("1")
        assert snapshot.__repr__() == protocol.Snapshot.deserialize(snapshot.serialize()).__repr__()
        break

