import json


def parse(json_snapshot):
    """extracts and returns the pose information from json_snapshot"""
    snapshot = json.loads(json_snapshot)
    pose = dict(user_id=snapshot['user_id'],
                datetime=snapshot['datetime'],
                result='pose',
                pose=snapshot['pose'])
    return json.dumps(pose)


parse.name = 'pose'
