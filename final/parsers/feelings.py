import json


def parse_feelings(json_snapshot):
    """extracts and returns the feelings information from json_snapshot"""
    message = json.loads(json_snapshot)
    if message['type'] != 'snapshot':  # ignoring non-snapshot messages
        return None
    pose = dict(type='feelings',
                user_id=message['user_id'],
                datetime=message['datetime'],
                feelings=message['feelings'])
    return json.dumps(pose)


parse_feelings.name = 'feelings'
