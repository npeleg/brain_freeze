import pathlib
import pytest
import threading
import time

from final import Reader
from final.utils import Connection, protocol

ADDRESS = '127.0.0.1', 5000


def test_client():
    reader = Reader('../sample.mind.gz')
    print("read user info from file")
    for snapshot in reader:
        print("producing user message")
        user_message = protocol.init_protocol_user(reader.user.user_id, reader.user.username,
                                                   reader.user.birthday, reader.user.gender)
        with Connection.connect(*ADDRESS) as connection:
            print("established connection")
            connection.send_message(protocol.serialize(user_message))
            config = protocol.deserialize_config(connection.receive_message())
            partial_snapshot = protocol.build_partial_snapshot(snapshot, config)
            connection.send_message(protocol.serialize(partial_snapshot))
        break
    path = pathlib.Path(tmp_path)
    dt = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(snapshot.datetime / 1000))
    path = path / str(reader.user.user_id) / str(dt) / "translation.txt"
    print(f'Is {str(path)} a file?')
    print(path.is_file())
    time.sleep(5)  # waiting for sever to write the file
    with open(path, 'r') as file:
        string = file.read()
        print(string)
        assert string == protocol.repr_protocol_snapshot(partial_snapshot)
