import json
from final.saver import Saver
from final.utils import DBManager
from .utils.simulate_process import run_subprocess

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


def tes_save_cli():
    db = DBManager(db_url)
    saver_process = run_subprocess("python -m final.saver run-saver "
                                   "mongodb://127.0.0.1:27017 rabbitmq://127.0.0.1:5672/")
    for result in parsed_results:
        _id = saver.save(result, parsed_results[result])
        assert db._get_result_by_id(_id) == json.loads(parsed_results[result])