import pathlib
import subprocess
import time
from datetime import datetime as dt
from final import client, Reader
from final.utils import protocol


ADDRESS = '127.0.0.1', 5000
SMALL_SAMPLE_PATH = "./tests/utils/small_sample.mind.gz"


def run_subprocess(command, in_background=False):
    command = [x for x in command.split(" ")]
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               close_fds=in_background)
    return process


def test_upload_sample():
    server_process = run_subprocess("python -m final run_server 127.0.0.1 5000 ./users", in_background=True)
    # out, err = server_process.communicate()
    # print("out: " + out.decode())
    # print("err: " + err.decode())
    time.sleep(1)  # waiting for server
    client.upload_sample(ADDRESS, SMALL_SAMPLE_PATH)

    # checking the written files
    t_reader = Reader(SMALL_SAMPLE_PATH)
    for snapshot in t_reader:
        partial_snapshot = protocol.build_partial_snapshot(snapshot, protocol.init_protocol_config(['pose']))
        timestamp = dt.fromtimestamp(snapshot.datetime / 1000)
        timestamp = timestamp.strftime('%Y-%m-%d_%H-%M-%S.%f')[:-3]
        path = pathlib.Path("./users")
        path = path / str(t_reader.user.user_id) / str(timestamp) / "translation.txt"
        with open(path, 'r') as file:
            assert file.read() == protocol.repr_protocol_snapshot(partial_snapshot)
    server_process.terminate()
