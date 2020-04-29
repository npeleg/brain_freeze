import json
import threading
from ..parsers import Parsers
from ..utils import Listener, Logger, MQManager, protocol

logger = Logger(__name__).logger


def build_json_message(user, snapshot):
    message = dict(user_id=user.user_id,
                   username=user.username,
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


class ClientThread(threading.Thread):
    def __init__(self, client_connection, mq, parsers):
        threading.Thread.__init__(self)
        self.client_socket = client_connection
        self.mq = mq
        self.parsers = parsers

    def run(self):
        # receiving 'user' message from client:
        user = protocol.deserialize_user(self.client_socket.receive_message())

        # sending 'config' message to client:
        config = protocol.init_protocol_config(self.parsers)
        self.client_socket.send_message(protocol.serialize(config))

        # receiving 'snapshot' message from client:
        snapshot = protocol.deserialize_snapshot(self.client_socket.receive_message())

        # publishing user and snapshot data to message queue:
        json_message = build_json_message(user, snapshot)
        logger.info('sending snapshot to message queue')
        self.mq.publish_to_incoming_topic(json_message)


def run_server(address, url):
    logger.info('initializing message queue')
    mq = MQManager(url)
    parsers = Parsers().get_parsers_names()
    with Listener(port=address[1], host=address[0]) as listener:
        logger.info('server is running')
        while True:
            client_connection = listener.accept()
            new_thread = ClientThread(client_connection, mq, parsers)
            new_thread.start()
