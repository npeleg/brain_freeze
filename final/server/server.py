import json
import flask
from ..parsers import Parsers
from ..utils import Logger, MQManager, protocol

logger = Logger(__name__).logger
app = flask.Flask(__name__)
user_function = None
message_queue = None
parsers = []


def build_json_message(user, snapshot):
    message = dict(user_id=user.user_id,
                   username=user    .username,
                   birthday=user.birthday,
                   gender=user.gender.name,
                   datetime=snapshot.datetime,
                   pose=dict(translation=dict(x=snapshot.pose.translation.x,
                                              y=snapshot.pose.translation.y,
                                              z=snapshot.pose.translation.z),
                             rotation=dict(x=snapshot.pose.rotation.x,
                                           y=snapshot.pose.rotation.y,
                                           z=snapshot.pose.rotation.z,
                                           w=snapshot.pose.rotation.w)),
                   # TODO color and depth images
                   feelings=dict(hunger=snapshot.feelings.hunger,
                                 thirst=snapshot.feelings.thirst,
                                 exhaustion=snapshot.feelings.exhaustion,
                                 happiness=snapshot.feelings.happiness)
                   )
    return json.dumps(message)


@app.route('/config')
def return_parsers():
    global parsers
    logger.info('sending parsers list to client')
    return flask.jsonify({'parsers': parsers, 'error': None})


@app.route('/snapshots', methods=['POST'])
def receive_snapshot():
    global message_queue, user_function
    try:
        request = flask.request.get_json(force=True)
        print(request)
        if user_function:
            print('user function is not none')
            user_function(request['snapshot'])
        else:
            print("1")
            user_message = protocol.deserialize_user(request['user'])
            print("2")
            snapshot_message = protocol.deserialize_snapshot(request['snapshot'])
            print("3")
            json_message = build_json_message(user_message, snapshot_message)
            logger.info('sending snapshot to message queue')
            message_queue.publish_to_incoming_topic(json_message)
        return flask.jsonify({'result': 'accepted', 'error': None}), 201
    except Exception as error:
        print('exception')
        return flask.jsonify({'result': None, 'error': str(error)}), 404


def run_server(host, port, publish):
    global message_queue, user_function, parsers
    try:
        message_queue = MQManager(publish)
        logger.info('initialized message queue')
    except AttributeError:
        logger.info('a user function was passed')
        user_function = publish
    parsers = Parsers().get_parsers_names()
    logger.info('starting the server')
    app.run(host=host, port=port)
