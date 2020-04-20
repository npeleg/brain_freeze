import json


def parse_pose(json_snapshot):
    """extracts and returns the pose information from json_snapshot"""
    message = json.loads(json_snapshot)
    if message['type'] != 'snapshot':  # ignoring non-snapshot messages
        return None
    pose = dict(type='pose',
                user_id=message['user_id'],
                datetime=message['datetime'],
                pose=message['pose'])
    return json.dumps(pose)


parse_pose.name = 'pose'
