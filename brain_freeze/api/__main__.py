import click
import sys
from . import api


@click.group()
def main():
    pass


@main.command('run-server')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1',
              help='IP address of the server')
@click.option('-p', '--port', type=click.INT, default=5000,
              help='port of the server')
@click.option('-d', '--database', type=click.STRING,
              default='mongodb://localhost:27017')
def run_api_server(host, port, database):
    """ Listen on HOST:PORT and serve data from DATABASE"""
    try:
        api.run_api_server(host, port, database)
    except Exception as error:
        print(f'Error during run_api_server command: {error}')
        return 1


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        click.echo(f'ERROR: {err}')
        sys.exit(1)
