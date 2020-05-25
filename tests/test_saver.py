import json
from brain_freeze.saver import Saver
from brain_freeze.utils import DBManager
from utils.simulate_process import run_subprocess, sleep

parsed_pose = json.dumps(dict(user_id=1, datetime=2, result='pose', pose=3))
parsed_feelings = json.dumps(dict(user_id=1, datetime=2, result='feelings', feelings=4))
parsed_results = {'pose': parsed_pose, 'feelings': parsed_feelings}

db_url = 'mongodb://127.0.0.1:27017'


def test_save():
    db = DBManager(db_url)
    saver = Saver(db_url)
    for result in parsed_results:
        _id = saver.save(result, parsed_results[result])
        assert db._get_result_by_id(_id) == json.loads(parsed_results[result])


def test_save_cli(tmp_path):
    for result in parsed_results:
        file = tmp_path / f'{result}.result'
        with open(str(file), 'w') as f:
            f.write(parsed_results[result])
        saver_process = run_subprocess("python -m brain_freeze.saver save "
                                       f"-d mongodb://127.0.0.1:27017 {result} {str(file)}")
        saver_process.wait()
        saver_process.terminate()
        out, err = saver_process.communicate()
        assert err.decode() == ''
        assert 'saved to db' in out.decode()


def test_run_saver_cli():
    processes = []
    for result in parsed_results:
        saver_process = run_subprocess("python -m brain_freeze.saver run-saver "
                                       "mongodb://127.0.0.1:27017 rabbitmq://127.0.0.1:5672/")
        processes.append(saver_process)
    sleep(5)
    for process in processes:
        process.terminate()
        out, err = process.communicate()
        assert err.decode() == ''
        assert 'running...' in out.decode()
