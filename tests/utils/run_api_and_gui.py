from simulate_process import run_subprocess, sleep

api_process = run_subprocess("python -m brain_freeze.api run-server")
sleep(2)
gui_process = run_subprocess("python -m brain_freeze.gui run-server")
sleep(2)
