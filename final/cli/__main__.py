import click
import sys
import requests


@click.group()
def main():
    pass


@main.command('get_users')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1', help='IP address of the server')
@click.option('-p', '--port', type=click.INT, default=5000, help='port of the server')
def client_upload_sample(host, port):
    """ Get a list of all the users. """
    try:
        r = requests.get(f'http://{host}:{port}/users')
        print(r.json())
    except Exception as error:
        print(f'Error: {error}')
        return 1


@main.command('get_user')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1', help='IP address of the server')
@click.option('-p', '--port', type=click.INT, default=5000, help='port of the server')
@click.argument('user_id', type=click.INT)
def client_upload_sample(host, port, user_id):
    """ Get info about the user whose ID is USER_ID. """
    try:
        r = requests.get(f'http://{host}:{port}/users/{user_id}')
        print(r.json())
    except Exception as error:
        print(f'Error: {error}')
        return 1


@main.command('get_snapshots')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1', help='IP address of the server')
@click.option('-p', '--port', type=click.INT, default=5000, help='port of the server')
@click.argument('user_id', type=click.INT)
def client_upload_sample(host, port, user_id):
    """ Get a list of all the snapshots of USER_ID. """
    try:
        r = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots')
        print(r.json())
    except Exception as error:
        print(f'Error: {error}')
        return 1


@main.command('get_snapshot')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1', help='IP address of the server')
@click.option('-p', '--port', type=click.INT, default=5000, help='port of the server')
@click.argument('user_id', type=click.INT)
@click.argument('snapshot_id', type=click.INT)
def client_upload_sample(host, port, user_id, snapshot_id):
    """ Get a list of the results in snapshot SNAPSHOT_ID of USER_ID. """
    try:
        r = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}')
        print(r.json())
    except Exception as error:
        print(f'Error: {error}')
        return 1


@main.command('get_result')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1', help='IP address of the server')
@click.option('-p', '--port', type=click.INT, default=5000, help='port of the server')
@click.option('-s', '--save', type=click.STRING)
@click.argument('user_id', type=click.INT)
@click.argument('snapshot_id', type=click.INT)
@click.argument('result', type=click.STRING)
def client_upload_sample(host, port, user_id, snapshot_id, result, save):
    """ Get the RESULT of snapshot SNAPSHOT_ID of USER_ID, optionally saving it to SAVE path. """
    try:
        r = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}/{result}')
        if save:
            with open(save, 'w') as file:
                file.write(r.json())
        else:
            print(r.json())
    except Exception as error:
        print(f'Error: {error}')
        return 1


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        click.echo(f'ERROR: {err}')
        sys.exit(1)
