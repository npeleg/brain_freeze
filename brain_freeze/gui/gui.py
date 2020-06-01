import requests
from flask import Flask, render_template
from ..utils import Logger

logger = Logger(__name__).logger
app = Flask(__name__)
api_host = ''
api_port = 0
gui_host = ''
gui_port = 0


def send_and_handle_request(request):
    try:
        r = requests.get(request).json()
        if r['result']:
            return r['result'], False
        else:
            logger.error(f"{r['error']}")
            return render_template('error.html'), True
    except Exception as error:
        logger.error(f"{error}")
        return render_template('error.html'), True


@app.route('/users', methods=['GET'])
@app.route('/', methods=['GET'])
def index():
    request = f'http://{api_host}:{api_port}/users'
    result, error = send_and_handle_request(request)
    if error:
        return result
    for user in result:
        user['link'] = f"http://{gui_host}:{gui_port}/users/{user['user_id']}"
    return render_template('index.html', users=result)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    request = f'http://{api_host}:{api_port}/users/{user_id}'
    result, error = send_and_handle_request(request)
    if error:
        return result
    snapshots_link = f"http://{gui_host}:{gui_port}/users/{user_id}/snapshots"
    return render_template('user.html', username=result['username'],
                           user_id=user_id, birthday=result['birthday'],
                           gender=result['gender'].title(),
                           snapshots_link=snapshots_link)


@app.route('/users/<int:user_id>/snapshots', methods=['GET'])
def get_snapshots(user_id):
    request = f'http://{api_host}:{api_port}/users/{user_id}/snapshots'
    result, error = send_and_handle_request(request)
    if error:
        return result
    for snapshot in result:
        snapshot['link'] = f"http://{gui_host}:{gui_port}/users/{user_id}/" \
                           f"snapshots/{snapshot['snapshot_id']}"
    return render_template('snapshot_list.html', snapshot_list=result)


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>', methods=['GET'])
def get_snapshot(user_id, snapshot_id):
    request = f'http://{api_host}:{api_port}/users/{user_id}/' \
              f'snapshots/{snapshot_id}'
    result, error = send_and_handle_request(request)
    if error:
        return result
    results_dict = {}
    for res in result['result_names']:
        request = f'http://{api_host}:{api_port}/users/{user_id}/' \
                  f'snapshots/{snapshot_id}/{res}'
        result, error = send_and_handle_request(request)
        if error:
            return result
        results_dict[res] = result[res]
    return render_template('snapshot.html', results=results_dict,
                           snapshot_id=snapshot_id)


def run_server(host, port, _api_host, _api_port):
    """ listen on host:port and serve data from database_url """
    global api_host, api_port, gui_host, gui_port
    api_host = _api_host
    api_port = _api_port
    gui_host = host
    gui_port = port
    app.run(host=host, port=port)
