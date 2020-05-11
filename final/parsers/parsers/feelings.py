import json


def parse(json_snapshot):
    """extracts and returns the feelings information from json_snapshot"""
    message = json.loads(json_snapshot)
    pose = dict(user_id=message['user_id'],
                result='feelings',
                datetime=message['datetime'],
                feelings=message['feelings'])
    return json.dumps(pose)


parse.name = 'feelings'
