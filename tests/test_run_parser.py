import time
import subprocess


def run_subprocess(command):
    command = [x for x in command.split(" ")]
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               close_fds=True)
    return process


def test_run_parser():
    process = run_subprocess("python -m final.parsers run_parser pose rabbitmq://127.0.0.1:5672/")
    time.sleep(5)
    process.terminate()
    out, err = process.communicate()
    assert 'starting to consume' in out.decode()
    assert err == b''
