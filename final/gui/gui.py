import requests
from flask import Flask, render_template
from ..utils import Logger

logger = Logger(__name__).logger
app = Flask(__name__)
api_host = ''
api_port = 0


def send_and_handle_request(request, page_name):
    try:
        r = requests.get(request).json()
        if r['result']:
            print('correct')
            print(r['result'])
            return render_template(f'{page_name}.html', result=r['result'])
        else:
            logger.error(f"{r['error']}")
            print('here')
            return render_template('error.html')
    except Exception as error:
        logger.error(f"{error}")
        print('there')
        return render_template('error.html')


@app.route('/users', methods=['GET'])
@app.route('/', methods=['GET'])
def index():
    request = f'http://{api_host}:{api_port}/users'
    return send_and_handle_request(request, 'index')


def run_server(host, port, _api_host, _api_port):
    """ listen on host:port and serve data from database_url """
    global api_host, api_port
    api_host = _api_host
    api_port = _api_port
    app.run(host=host, port=port)
