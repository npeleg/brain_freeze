import pathlib
import pytest
import threading
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from final import Reader
from final.utils import Connection, protocol

ADDRESS = '127.0.0.1', 5000
DATA_DIR = "./users"


# @pytest.fixture()
def test_client():
    reader = Reader('../sample.mind.gz')
    print("read user info from file")
    for snapshot in reader:
        print("producing user message")
        user_message = protocol.User(reader.user.user_id, reader.user.username,
                                     reader.user.birthday, reader.user.gender)
        with Connection.connect(*ADDRESS) as connection:
            print("established connection")
            connection.send_message(user_message.serialize())
            config = protocol.Config.deserialize(connection.receive_message())
            # print(snapshot.color_image.pixels)  # TODO delete
            partial_snapshot = snapshot.build_partial_snapshot(config)
            # print(partial_snapshot.color_image.pixels)  # TODO delete
            connection.send_message(partial_snapshot.serialize())
        break
    path = pathlib.Path(DATA_DIR)
    dt = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(snapshot.datetime / 1000))
    path = path / str(reader.user.user_id) / str(dt) / "translation.txt"
    time.sleep(3)
    with open(path, 'r') as file:
        assert file.read() == snapshot.__repr__()


test_client()
