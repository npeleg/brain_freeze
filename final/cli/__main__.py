import click
import sys
import requests


def send_and_handle_request(request, is_list, file_path):
    try:
        r = requests.get(request).json()
        if r['result']:
            string_result = ""
            if is_list:
                for item in r['result']:
                    string_result += str(item) + '\n'
            else:
                string_result = r['result']
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(string_result)
            else:
                print(string_result)
        else:
            print(r['error'])
    except Exception as error:
        print(f'Error: {error}')
        return 1


@click.group()
def main():
    pass


@main.command('get-users')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1', help='IP address of the server')
@click.option('-p', '--port', type=click.INT, default=5000, help='port of the server')
def get_users(host, port):
    """ Get a list of all the users. """
    request = f'http://{host}:{port}/users'
    send_and_handle_request(request, is_list=True, file_path=None)


@main.command('get-user')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1', help='IP address of the server')
@click.option('-p', '--port', type=click.INT, default=5000, help='port of the server')
@click.argument('user_id', type=click.INT)
def get_user(host, port, user_id):
    """ Get info about the user whose ID is USER_ID. """
    request = f'http://{host}:{port}/users/{user_id}'
    send_and_handle_request(request, is_list=False, file_path=None)


@main.command('get-snapshots')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1', help='IP address of the server')
@click.option('-p', '--port', type=click.INT, default=5000, help='port of the server')
@click.argument('user_id', type=click.INT)
def get_snapshots(host, port, user_id):
    """ Get a list of all the snapshots of USER_ID. """
    request = f'http://{host}:{port}/users/{user_id}/snapshots'
    send_and_handle_request(request, is_list=True, file_path=None)


@main.command('get-snapshot')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1', help='IP address of the server')
@click.option('-p', '--port', type=click.INT, default=5000, help='port of the server')
@click.argument('user_id', type=click.INT)
@click.argument('snapshot_id', type=click.INT)
def get_snapshot(host, port, user_id, snapshot_id):
    """ Get a list of the results in snapshot SNAPSHOT_ID of USER_ID. """
    request = f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}'
    send_and_handle_request(request, is_list=False, file_path=None)


@main.command('get-result')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1', help='IP address of the server')
@click.option('-p', '--port', type=click.INT, default=5000, help='port of the server')
@click.option('-s', '--save', type=click.STRING)
@click.argument('user_id', type=click.INT)
@click.argument('snapshot_id', type=click.INT)
@click.argument('result', type=click.STRING)
def get_result(host, port, user_id, snapshot_id, result, save):
    """ Get the RESULT of snapshot SNAPSHOT_ID of USER_ID, optionally saving it to SAVE path. """
    request = f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}/{result}'
    send_and_handle_request(request, is_list=False, file_path=save)


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        click.echo(f'ERROR: {err}')
        sys.exit(1)
