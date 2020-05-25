import json


def parse(json_snapshot):
    """extracts and returns the feelings information from json_snapshot"""
    snapshot = json.loads(json_snapshot)
    feelings = dict(user_id=snapshot['user_id'],
                    datetime=snapshot['datetime'],
                    result='feelings',
                    feelings=snapshot['feelings'])
    return json.dumps(feelings)


parse.name = 'feelings'
