import click
import sys
from .server import run_server

@click.group()
def main():
    pass


@main.command('run_server')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1', help='IP address of the server')
@click.option('-p', '--port', type=click.INT, default=8000, help='port to be bound')
@click.argument('data_dir', type=click.STRING)
def server_run_server(host, port, data_dir):
    """ Serves DATA_DIR to clients. """
    try:
        run_server((host, int(port)), data_dir)
    except Exception as error:
        print(f'Error: {error}')
        return 1


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        click.echo(f'ERROR: {err}')
        sys.exit(1)