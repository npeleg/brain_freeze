from flask import Flask
from flask import jsonify
from datetime import datetime as dt
from ..utils import DBManager, Logger

logger = Logger(__name__).logger
app = Flask(__name__)
db = None


@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = db.get_all_users()
        output = []
        for user in users:
            output.append({'user_id': user['user_id'], 'name': user['username']})
        return jsonify({'result': output, 'error': None})
    except Exception as error:
        return jsonify({'result': None, 'error': str(error)}), 404


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = db.get_user(user_id)
        if user:
            output = user
        else:
            output = "No such user"
        return jsonify({'result': output, 'error': None})
    except Exception as error:
        return jsonify({'result': None, 'error': str(error)}), 404


@app.route('/users/<int:user_id>/snapshots', methods=['GET'])
def get_user_snapshots(user_id):
    try:
        snapshots_datetimes = get_user_snapshots(user_id)
        if snapshots_datetimes is None:
            output = "No such user"
        elif snapshots_datetimes == []:
            output = "User has no snapshots"
        else:
            output = []
            for datetime in snapshots_datetimes:
                _id = int(datetime.strftime('%Y-%m-%d_%H-%M-%S.%f'))
                output.append({'snapshot_id': _id, 'datetime': datetime})
        return jsonify({'result': output, 'error': None})
    except Exception as error:
        return jsonify({'result': None, 'error': str(error)}), 404


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>', methods=['GET'])
def get_snapshot_fields(user_id, snapshot_id):
    

def run_api_server(host, port, database_url):
    """ listen on host:port and serve data from database_url """
    global db
    db = DBManager(database_url)
    app.run(host=host, port=port)
