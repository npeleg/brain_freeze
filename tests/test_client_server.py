import pathlib
import subprocess
import time
from datetime import datetime as dt
from final import client, Reader
from final.utils import protocol


ADDRESS = '127.0.0.1', 8000
SMALL_SAMPLE_PATH = "./tests/utils/small_sample.mind.gz"


def run_subprocess(command):
    command = [x for x in command.split(" ")]
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               close_fds=True)
    return process


def test_upload_sample():
    server_process = run_subprocess("python -m final.server run_server rabbitmq://127.0.0.1:5672/")
    time.sleep(1)  # waiting for server
    client.upload_sample(ADDRESS, SMALL_SAMPLE_PATH)
    server_process.terminate()
    # out, err = server_process.communicate()
    # print("out: " + out.decode())
    # print("err: " + err.decode())

    # checking the written files
    t_reader = Reader(SMALL_SAMPLE_PATH)
    for snapshot in t_reader:
        partial_snapshot = protocol.build_partial_snapshot(snapshot, protocol.init_protocol_config(['pose']))
        timestamp = dt.fromtimestamp(snapshot.datetime / 1000)
        timestamp = timestamp.strftime('%Y-%m-%d_%H-%M-%S.%f')[:-3]
        path = pathlib.Path(DATA_PATH)
        path = path / str(t_reader.user.user_id) / str(timestamp) / "translation.txt"
        with open(path, 'r') as file:
            assert file.read() == protocol.repr_protocol_snapshot(partial_snapshot)
