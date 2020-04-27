import subprocess
import time
import multiprocessing
from final import utils

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


def func(data):
    print("OK")


def test_end_to_end():
    server_process = run_subprocess("python -m final.server run_server rabbitmq://127.0.0.1:5672/")
    time.sleep(1)  # waiting for server
    pose_process = run_subprocess("python -m final.parsers run_parser pose rabbitmq://127.0.0.1:5672/")
    time.sleep(1)
    mq = utils.MQManager('rabbitmq://127.0.0.1:5672/')
    p = multiprocessing.Process(target=mq.subscribe_to_topic('pose', func))
    p.start()
    time.sleep(2)
    p.terminate()
    p.join()
    client_process = run_subprocess("python -m final.client upload_sample " + SMALL_SAMPLE_PATH)
    pose_process.terminate()
    server_process.terminate()
    # out, err = server_process.communicate()
    # print("out: " + out.decode())
    # print("err: " + err.decode())
    assert 1 == 0
