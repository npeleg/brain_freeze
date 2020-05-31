import subprocess
import time
import pymongo

SMALL_SAMPLE_PATH = "./tests/utils/small_sample.mind.gz"


def run_subprocess(command):
    command = [x for x in command.split(" ")]
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               close_fds=True)
    return process


def test_end_to_end():
    # Clearing the db:
    client = pymongo.MongoClient('mongodb://localhost:27017')
    client.drop_database('db')

    # Starting to run services:
    saver_process = run_subprocess("python -m brain_freeze.saver run-saver "
                                   "mongodb://127.0.0.1:27017 rabbitmq://127.0.0.1:5672/")
    time.sleep(1)
    pose_process = run_subprocess("python -m brain_freeze.parsers run-parser pose rabbitmq://127.0.0.1:5672/")
    time.sleep(1)
    feelings_process = run_subprocess("python -m brain_freeze.parsers run-parser feelings rabbitmq://127.0.0.1:5672/")
    time.sleep(1)
    color_process = run_subprocess("python -m brain_freeze.parsers run-parser color_image rabbitmq://127.0.0.1:5672/")
    time.sleep(1)
    server_process = run_subprocess("python -m brain_freeze.server run-server rabbitmq://127.0.0.1:5672/")
    time.sleep(5)
    # Running the client:
    client_process = run_subprocess("python -m brain_freeze.client upload_sample " + SMALL_SAMPLE_PATH)
    time.sleep(350)

    # Running the api and cli:
    api_process = run_subprocess("python -m brain_freeze.api run-server")
    time.sleep(5)
    cli_users_process = run_subprocess("python -m brain_freeze.cli get-users")
    time.sleep(5)
    cli_user_process = run_subprocess("python -m brain_freeze.cli get-user 42")
    time.sleep(5)
    cli_snapshots_process = run_subprocess("python -m brain_freeze.cli get-snapshots 42")
    time.sleep(5)
    cli_snapshot_process = run_subprocess("python -m brain_freeze.cli get-snapshot 42 1575446887339")
    time.sleep(5)
    cli_result_process = run_subprocess("python -m brain_freeze.cli get-result 42 1575446887339 pose")
    time.sleep(5)

    # Checking the results:
    client_process.terminate()
    saver_process.terminate()
    pose_process.terminate()
    feelings_process.terminate()
    color_process.terminate()
    server_process.terminate()
    api_process.terminate()
    out, err = client_process.communicate()
    print("client out: " + out.decode())
    print("client err: " + err.decode())
    assert client_process.returncode == 0

    out, err = server_process.communicate()
    print("server out: " + out.decode())
    print("server err: " + err.decode())

    out, err = color_process.communicate()
    print("color out: " + out.decode())
    print("color err: " + err.decode())

    out, err = pose_process.communicate()
    print("pose out: " + out.decode())
    print("pose err: " + err.decode())

    out, err = feelings_process.communicate()
    print("feelings out: " + out.decode())
    print("feelings err: " + err.decode())

    out, err = saver_process.communicate()
    print("saver out: " + out.decode())
    print("saver err: " + err.decode())

    out, err = api_process.communicate()
    print("api out: " + out.decode())
    print("api err: " + err.decode())

    out, err = cli_users_process.communicate()
    print("cli_users out: " + out.decode())
    print("cli_users err: " + err.decode())
    assert b'Dan Gittik' in out

    out, err = cli_user_process.communicate()
    print("cli_user out: " + out.decode())
    print("cli_user err: " + err.decode())
    assert b'Dan Gittik' in out

    out, err = cli_snapshots_process.communicate()
    print("cli_snapshots_process out: " + out.decode())
    print("cli_snapshots_process err: " + err.decode())
    assert b'1575446887339' in out

    out, err = cli_snapshot_process.communicate()
    print("cli_snapshot_process out: " + out.decode())
    print("cli_snapshot_process err: " + err.decode())
    assert b'pose' in out
    assert b'feelings' in out

    out, err = cli_result_process.communicate()
    print("cli_result_process out: " + out.decode())
    print("cli_result_process err: " + err.decode())
    assert b'0.4873843491077423' in out
