import pathlib
from datetime import datetime
from flask import Flask

directory = ""
web = Flask(__name__)


@web.route('/')
def index():
    global directory
    _dir = directory
    data = b' \
            <html> \
                 <head> \
                    <title>Brain Computer Interface</title> \
                </head> \
                <body> \
                    <ul> '
    path = pathlib.Path(_dir)
    for entry in path.iterdir():
        if entry.is_dir():
            item_path = str(entry.relative_to(path)).encode()
            data += b'<li><a href=/users/' +\
                    item_path + b'>user ' + item_path + b'</a></li>'
    data += b'</ul></body></html>'
    return 200, data


@web.route('/users/<user_id>')
def user(user_id):
    global directory
    _dir = directory
    user_number = user_id
    user_path = pathlib.Path(str(_dir) + "/" + str(user_number))
    if not user_path.is_dir():
        data = b'Error: User Not Found'
    else:
        data = b'<html><head><title>Brain Computer Interface: User ' + str(
            user_number).encode() + b'</title></head><body><table>'
        for entry in user_path.iterdir():
            if entry.is_file():
                with entry.open() as _file:
                    line = _file.readline()
                    if line:
                        dt = datetime.strptime(entry.stem, '%Y-%m-%d_%H-%M-%S')
                        timestamp = f'{dt:%Y-%m-%d %H:%M:%S}'
                        data += b'<tr><td>' + timestamp.encode() +\
                                b'</td><td> ' + line.encode() + b'</td></tr>'
    data += b'</tr></table></body></html>'
    return 200, data


def run_webserver(address, data_dir):
    try:
        global directory
        directory = data_dir  # TODO make one liner
        print("entering .run:")
        web.run(address)
        print("exiting .run:")
    except Exception as error:
        print(f'ERROR: {error}')
        return 1
