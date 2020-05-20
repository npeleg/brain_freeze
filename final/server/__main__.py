import click
import sys
from .server import run_server


@click.group()
def main():
    pass


@main.command('run-server')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1', help='IP address of the server')
@click.option('-p', '--port', type=click.INT, default=8000, help='port to be bound')
@click.argument('url', type=click.STRING)
def server_run_server(host, port, url):
    """ Passes snapshots received from clients to the message queue specified in url. """
    try:
        print('running from cli')
        run_server(host, int(port), url)
    except Exception as error:
        print(f'Error: {error}')
        return 1


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        click.echo(f'ERROR: {err}')
        sys.exit(1)
