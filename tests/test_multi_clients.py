from utils.simulate_process import run_subprocess, sleep, SMALL_SAMPLE_PATH


def test_multi_client():
    server_process = run_subprocess("python -m final.server run-server dummy")
    sleep(2)
    client_process1 = run_subprocess("python -m final.client upload_sample " + SMALL_SAMPLE_PATH)
    client_process2 = run_subprocess("python -m final.client upload_sample " + SMALL_SAMPLE_PATH)
    client_process3 = run_subprocess("python -m final.client upload_sample " + SMALL_SAMPLE_PATH)
    sleep(300)
    client_process1.terminate()
    client_process2.terminate()
    client_process3.terminate()
    server_process.terminate()
    assert client_process1.returncode == 0
    assert client_process2.returncode == 0
    assert client_process3.returncode == 0
