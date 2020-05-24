import subprocess
import time
from final.client import upload_sample
SMALL_SAMPLE_PATH = "./tests/utils/small_sample.mind.gz"


def run_subprocess(command):
    command = [x for x in command.split(" ")]
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               close_fds=True)
    return process


def test_client():
    # running the server with a dummy user function
    server_process = run_subprocess("python -m final.server run-server dummy")
    time.sleep(1)

    return_code = upload_sample(host='127.0.0.1', port=8000, path=SMALL_SAMPLE_PATH)
    assert return_code == 0

    client_process = run_subprocess("python -m final.client upload_sample " + SMALL_SAMPLE_PATH)
    time.sleep(300)
    client_process.terminate()
    out, err = client_process.communicate()
    print("client out: " + out.decode())
    print("client err: " + err.decode())
    server_process.terminate()
    out, err = server_process.communicate()
    print("server out: " + out.decode())
    print("server err: " + err.decode())
    assert client_process.returncode == 0
    assert 1 == 0

