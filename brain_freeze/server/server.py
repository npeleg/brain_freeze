import json
import flask
import pathlib
import sys
from ..parsers import Parsers
from ..utils import Logger, MQManager, protocol

logger = Logger(__name__).logger
app = flask.Flask(__name__)
user_function = None
message_queue = None
parsers = []
data_volume = './data_volume'


def build_user_json(user):
    message = dict(user_id=user.user_id,
                   username=user.username,
                   birthday=user.birthday,
                   gender=user.gender.name,
                   )
    return json.dumps(message)


def build_snapshot_json(snapshot, user_id, path,
                        color_image_path, depth_image_path):
    message = dict(user_id=user_id,
                   datetime=snapshot.datetime,
                   pose=dict(translation=dict(x=snapshot.pose.translation.x,
                                              y=snapshot.pose.translation.y,
                                              z=snapshot.pose.translation.z),
                             rotation=dict(x=snapshot.pose.rotation.x,
                                           y=snapshot.pose.rotation.y,
                                           z=snapshot.pose.rotation.z,
                                           w=snapshot.pose.rotation.w)),
                   color_image=dict(width=snapshot.color_image.width,
                                    height=snapshot.color_image.height,
                                    dir_path=path,
                                    file_path=color_image_path),
                   depth_image=dict(width=snapshot.depth_image.width,
                                    height=snapshot.depth_image.height,
                                    dir_path=path,
                                    file_path=depth_image_path),
                   feelings=dict(hunger=snapshot.feelings.hunger,
                                 thirst=snapshot.feelings.thirst,
                                 exhaustion=snapshot.feelings.exhaustion,
                                 happiness=snapshot.feelings.happiness)
                   )
    return json.dumps(message)


def store_images(snapshot, user_id):
    """ stores color_image and depth_image,
    if exist in snapshot, and returns their paths"""
    try:
        path = pathlib.Path(data_volume + f'/{user_id}/{snapshot.datetime}')
        path.mkdir(parents=True, exist_ok=True)
        if 'color_image' in parsers:
            color_path = path / 'color_image'
            with color_path.open('wb') as file:
                file.write(snapshot.color_image.data)
        else:
            color_path = None
        if 'depth_image' in parsers:
            depth_path = path / 'depth_image'
            with depth_path.open('wb') as file:
                file.write(snapshot.depth_image.data)
        else:
            depth_path = None
        return str(path), str(color_path), str(depth_path)
    except Exception as error:
        logger.error('failed to save images:')
        logger.error(str(error))
        return None, None, None


@app.route('/config')
def send_parsers():
    logger.info('sending parsers list to client')
    logger.debug(parsers)
    return flask.jsonify({'result': 'accepted',
                          'parsers': parsers, 'error': None})


@app.route('/users', methods=['POST'])
def receive_user():
    global message_queue, user_function
    try:
        request = flask.request.data
        user_message = protocol.deserialize_user(request)
        if not user_function:
            json_message = build_user_json(user_message)
            logger.info('sending user to message queue')
            message_queue.publish_to_user_topic(json_message)
        return flask.jsonify({'result': 'accepted', 'error': None}), 201
    except Exception as error:
        logger.error("error: ")
        logger.error(str(error.__repr__))
        return flask.jsonify({'result': None, 'error': str(error)}), 404


@app.route('/snapshots/<int:user_id>', methods=['POST'])
def receive_snapshot(user_id):
    global message_queue, user_function
    try:
        sys.stdout.flush()
        request = flask.request.data
        snapshot_message = protocol.deserialize_snapshot(request)
        if user_function:
            try:
                user_function(snapshot_message)
            except Exception as error:
                logger.info('error in user function or user'
                            'passed a non callable object:')
                logger.info(str(error))
        else:
            path, color_path, depth_path = store_images(snapshot_message,
                                                        user_id)
            json_message = build_snapshot_json(snapshot_message,
                                               user_id, path,
                                               color_path, depth_path)
            logger.info('sending snapshot to message queue')
            message_queue.publish_to_snapshot_topic(json_message)
        return flask.jsonify({'result': 'accepted', 'error': None}), 201
    except Exception as error:
        logger.error("error: ")
        logger.error(str(error.__repr__))
        return flask.jsonify({'result': None, 'error': str(error)}), 404


def run_server(host, port, publish):
    global message_queue, user_function, parsers
    try:
        message_queue = MQManager(publish)
    except AttributeError:
        logger.info('a user function was passed')
        user_function = publish
    parsers = Parsers().get_parsers_names()
    logger.info('starting the server')
    app.run(host=host, port=port)
