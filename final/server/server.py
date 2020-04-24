import json
import threading
from .message_queue_manager import MQManager
from ..parsers import Parsers
from ..utils import Listener, protocol, Logger

logger = Logger(__name__).logger


class ClientThread(threading.Thread):
    def __init__(self, client_connection, message_queue):
        threading.Thread.__init__(self)
        self.client_socket = client_connection
        self.message_queue = message_queue

    def run(self):
        # receiving 'user' message from client:
        user = protocol.deserialize_user(self.client_socket.receive_message())

        # sending 'config' message to client:
        # TODO config = protocol.init_protocol_config(Parsers().get_parsers_names())
        config = protocol.init_protocol_config({'pose'})
        self.client_socket.send_message(protocol.serialize(config))

        # receiving 'snapshot' message from client:
        snapshot = protocol.deserialize_snapshot(self.client_socket.receive_message())

        # publishing user and snapshot data to message queue:
        message = dict(type='snapshot',
                       user_id=user.user_id,
                       username=user.username,
                       birthday=user.birthday,
                       gender=user.gender,
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
        json_message = json.dumps(message)
        logger.info('sending snapshot to message queue')
        self.message_queue.send(json_message)


def run_server(address, url):
    logger.info('initializing message queue')
    message_queue = MQManager(url)
    with Listener(port=address[1], host=address[0]) as listener:
        logger.info('server is running')
        while True:
            client_connection = listener.accept()
            new_thread = ClientThread(client_connection, message_queue)
            new_thread.start()
