import subprocess
import time

SMALL_SAMPLE_PATH = "./tests/utils/small_sample.mind.gz"


def run_subprocess(command):
    command = [x for x in command.split(" ")]
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               close_fds=True)
    return process


def test_end_to_end():
    saver_process = run_subprocess("python -m final.saver run_saver database rabbitmq://127.0.0.1:5672/")
    time.sleep(1)
    pose_process = run_subprocess("python -m final.parsers run_parser pose rabbitmq://127.0.0.1:5672/")
    time.sleep(1)
    feelings_process = run_subprocess("python -m final.parsers run_parser feelings rabbitmq://127.0.0.1:5672/")
    time.sleep(1)
    server_process = run_subprocess("python -m final.server run_server rabbitmq://127.0.0.1:5672/")
    time.sleep(1)  # waiting for server
    client_process = run_subprocess("python -m final.client upload_sample " + SMALL_SAMPLE_PATH)
    time.sleep(30)
    client_process.terminate()
    saver_process.terminate()
    pose_process.terminate()
    feelings_process.terminate()
    server_process.terminate()
    out, err = client_process.communicate()
    print("client out: " + out.decode())
    print("client err: " + err.decode())
    out, err = server_process.communicate()
    print("server out: " + out.decode())
    print("server err: " + err.decode())
    out, err = pose_process.communicate()
    print("pose out: " + out.decode())
    print("pose err: " + err.decode())
    out, err = saver_process.communicate()
    print("saver out: " + out.decode())
    print("saver err: " + err.decode())
    assert client_process.returncode == 0
    # assert 'OK' in out.decode()
