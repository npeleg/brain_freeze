import json


class PoseParser:
    fields = ['translation', 'rotation']

    @classmethod
    def parse_translation(cls, context, snapshot):
        f = {'x': snapshot.pose.translation[0], 'y': snapshot.pose.translation[1],
             'z': snapshot.pose.translation[2]}
        context.save('translation.json', json.dumps(f))

    @classmethod
    def parse_rotation(cls, context, snapshot):
        context.save('rotation.json', json.dumps(dict(
            x=snapshot.pose.rotation[0],
            y=snapshot.pose.rotation[1],
            z=snapshot.pose.rotation[2],
            w=snapshot.pose.rotation[3],
        )))
