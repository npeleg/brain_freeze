import subprocess
import time


def run_subprocess(command):
    command = [x for x in command.split(" ")]
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               close_fds=True)
    return process


# Running the API server:
api_process = run_subprocess("python -m brain_freeze.api run-server")
time.sleep(1)

# Running the GUI server:
gui_process = run_subprocess("python -m brain_freeze.gui run-server")
time.sleep(1)

# Starting the saver:
saver_process = run_subprocess("python -m brain_freeze.saver run-saver "
                               "mongodb://127.0.0.1:27017 rabbitmq://127.0.0.1:5672/")
time.sleep(1)

# Starting the pose parser:
pose_process = run_subprocess("python -m brain_freeze.parsers run-parser pose rabbitmq://127.0.0.1:5672/")
time.sleep(1)

# Starting the feelings parser:
feelings_process = run_subprocess("python -m brain_freeze.parsers run-parser feelings rabbitmq://127.0.0.1:5672/")
time.sleep(1)

# Starting the color image parser:
color_process = run_subprocess("python -m brain_freeze.parsers run-parser color_image rabbitmq://127.0.0.1:5672/")
time.sleep(1)

# Starting the server:
server_process = run_subprocess("python -m brain_freeze.server run-server rabbitmq://127.0.0.1:5672/")
time.sleep(3)

print("You're good to go!")
print("You can now start the client and see the results in your browser at localhost:8080")
