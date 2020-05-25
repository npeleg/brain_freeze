from brain_freeze.client import upload_sample
from utils.simulate_process import run_subprocess, sleep, SMALL_SAMPLE_PATH


def test_client():
    # running the server with a dummy user function
    server_process = run_subprocess("python -m brain_freeze.server run-server dummy")
    sleep(2)

    client_process = run_subprocess("python -m brain_freeze.client upload_sample " + SMALL_SAMPLE_PATH)
    client_process.wait()
    client_process.terminate()
    out, err = client_process.communicate()
    assert client_process.returncode == 0

    return_code = upload_sample(host='127.0.0.1', port=8000, path=SMALL_SAMPLE_PATH)
    assert return_code == 0

    server_process.terminate()

