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


def sleep(duration):
    time.sleep(duration)
