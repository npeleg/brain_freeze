from flask import Flask, send_from_directory
from flask import jsonify
from datetime import datetime as dt
from ..utils import DBManager, Logger

logger = Logger(__name__).logger
app = Flask(__name__)
db = None
data_volume = '/data_volume'


def to_datetime(timestamp, milliseconds):
    if milliseconds:
        return dt.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d_%H-%M-%S.%f')[:-3]
    return dt.fromtimestamp(timestamp).strftime('%Y-%m-%d')


@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = db.get_all_users()
        output = []
        for user in users:
            output.append({'user_id': user['user_id'], 'username': user['username']})
        return jsonify({'result': output, 'error': None})
    except Exception as error:
        return jsonify({'result': None, 'error': str(error)}), 404


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = db.get_user_data(user_id)
        if user:
            user['birthday'] = to_datetime(user['birthday'], milliseconds=False)
            output = user
        else:
            output = "No such user"
        return jsonify({'result': output, 'error': None})
    except Exception as error:
        return jsonify({'result': None, 'error': str(error)}), 404


@app.route('/users/<int:user_id>/snapshots', methods=['GET'])
def get_user_snapshots(user_id):
    try:
        snapshot_ids = db.get_user_snapshots(user_id)
        output = []
        for _id in snapshot_ids:
            datetime = to_datetime(_id, milliseconds=True)
            output.append({'snapshot_id': _id, 'datetime': datetime})
        return jsonify({'result': output, 'error': None})
    except Exception as error:
        return jsonify({'result': None, 'error': str(error)}), 404


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>', methods=['GET'])
def get_snapshot_fields(user_id, snapshot_id):
    try:
        datetime = to_datetime(snapshot_id, milliseconds=True)
        output = {'snapshot_id': snapshot_id, 'datetime': datetime}
        results_names = db.get_available_results(user_id, snapshot_id)
        output['result_names'] = results_names
        return jsonify({'result': output, 'error': None})
    except Exception as error:
        return jsonify({'result': None, 'error': str(error)})


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>', methods=['GET'])
def get_result(user_id, snapshot_id, result_name):
    try:
        output = db.get_result(user_id, snapshot_id, result_name)
        return jsonify({'result': output, 'error': None})
    except Exception as error:
        return jsonify({'result': None, 'error': str(error)})


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>/<data_path>', methods=['GET'])
def get_data(user_id, snapshot_id, result_name, data_path):
    send_from_directory(directory=data_volume + f'{user_id}/{snapshot_id}', filename=data_path, as_attachment=True)


def run_api_server(host, port, database_url):
    """ listen on host:port and serve data from database_url """
    global db
    db = DBManager(database_url)
    app.run(host=host, port=port)
