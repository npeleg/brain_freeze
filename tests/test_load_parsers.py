import json
from final.parsers import Parsers

raw = json.dumps(dict(user_id=1, datetime=2, pose=3, feelings=4))
parsed_pose = json.dumps(dict(user_id=1, datetime=2, pose=3))
parsed_feelings = json.dumps(dict(user_id=1, datetime=2, feelings=4))


def test_load_parsers():
    parsers = Parsers().parsers_dict
    assert parsers['pose'](raw) == parsed_pose
    assert parsers['feelings'](raw) == parsed_feelings
