import json
from brain_freeze.parsers import Parsers
from utils.simulate_process import run_subprocess, sleep

raw = json.dumps(dict(user_id=1, datetime=2, pose=3, feelings=4))
parsed_pose = json.dumps(dict(user_id=1, datetime=2, result='pose', pose=3))
parsed_feelings = json.dumps(dict(user_id=1, datetime=2,
                                  result='feelings', feelings=4))
parsed_results = {'pose': parsed_pose, 'feelings': parsed_feelings}


def test_load_parsers():
    parsers_dict = Parsers().parsers_dict
    for parser in parsed_results:
        assert parsers_dict[parser](raw) == parsed_results[parser]


def test_parse():
    parsers = Parsers()
    for parser in parsed_results:
        assert parsers.parse(parser, raw) == parsed_results[parser]


def test_parse_cli(tmp_path):
    file = tmp_path / 'file.txt'
    with open(str(file), 'w') as f:
        f.write(raw)
    for parser in parsed_results:
        parser_proc = run_subprocess(f"python -m brain_freeze.parsers parse"
                                     f" {parser} {str(file)}")
        parser_proc.wait()
        parser_proc.terminate()
        out, err = parser_proc.communicate()
        print(out.decode())
        assert err.decode() == ''
        assert out.decode()[:-1] == parsed_results[parser]


# def test_parse_to_file(tmp_path):
#    src_file = tmp_path / 'src.txt'
#    dst_file = tmp_path / 'dst.txt'
#    with open(str(src_file), 'w') as f:
#        f.write(raw)
#    for parser in parsed_results:
#        parser_proc = run_subprocess(f"python -m brain_freeze.parsers parse "
#                                     f"{parser} {str(src_file)} > "
#                                     f "{str(dst_file)}")
#        parser_proc.wait()
#        parser_proc.terminate()
#        out, err = parser_proc.communicate()
#        assert err.decode() == ''
#        with open(str(dst_file), 'r') as file:
#            assert file.read() == parsed_results[parser]


def test_run_parser():
    processes = []
    for parser in parsed_results:
        parser_process = run_subprocess(f"python -m brain_freeze.parsers "
                                        f"run-parser {parser} "
                                        f"rabbitmq://127.0.0.1:5672/")
        processes.append(parser_process)
    sleep(5)
    for process in processes:
        process.terminate()
        out, err = process.communicate()
        assert err.decode() == ''
        assert 'running...' in out.decode()
