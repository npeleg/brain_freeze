import json


def parse(json_snapshot):
    """extracts and returns the pose information from json_snapshot"""
    message = json.loads(json_snapshot)
    pose = dict(user_id=message['user_id'],
                result='pose',
                datetime=message['datetime'],
                pose=message['pose'])
    return json.dumps(pose)


parse.name = 'pose'
