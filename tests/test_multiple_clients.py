from utils.simulate_process import run_subprocess, sleep, SMALL_SAMPLE_PATH

process_num = 3


def test_multi_client():
    server_process =\
        run_subprocess("python -m brain_freeze.server run-server dummy")
    sleep(2)

    processes = []
    for i in range(process_num):
        client_process = run_subprocess("python -m brain_freeze.client "
                                        "upload_sample " + SMALL_SAMPLE_PATH)
        processes.append(client_process)

    for process in processes:
        process.wait()
        process.terminate()
        process.communicate()
        assert process.returncode == 0

    server_process.terminate()
