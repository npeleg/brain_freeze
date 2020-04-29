import subprocess
import time
import multiprocessing
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from final import client, utils

ADDRESS = '127.0.0.1', 8000
SMALL_SAMPLE_PATH = "./tests/utils/small_sample.mind.gz"
DATA_PATH = './users'


def run_subprocess(command):
    command = [x for x in command.split(" ")]
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               close_fds=True)
    return process


def test_end_to_end():
    pose_process = run_subprocess("python -m final.parsers run_parser pose rabbitmq://127.0.0.1:5672/")
    time.sleep(1)
    saver_process = run_subprocess("python -m final.saver run_saver database rabbitmq://127.0.0.1:5672/")
    time.sleep(1)
    server_process = run_subprocess("python -m final.server run_server rabbitmq://127.0.0.1:5672/")
    time.sleep(1)  # waiting for server
    # client.upload_sample(ADDRESS, SMALL_SAMPLE_PATH)
    client_process = run_subprocess("python -m final.client upload_sample " + SMALL_SAMPLE_PATH)
    time.sleep(60)
    client_process.terminate()
    saver_process.terminate()
    pose_process.terminate()
    server_process.terminate()
    out, err = client_process.communicate()
    assert client_process.returncode == 0
    out, err = server_process.communicate()
    print("server out: " + out.decode())
    print("server err: " + err.decode())
    out, err = pose_process.communicate()
    print("pose out: " + out.decode())
    print("pose err: " + err.decode())
    out, err = saver_process.communicate()
    print("saver out: " + out.decode())
    print("saver err: " + err.decode())
    # assert 'OK' in out.decode()


test_end_to_end()
