import click
import sys
from . import gui


@click.group()
def main():
    pass


@main.command('run-server')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1', help='IP address of the server')
@click.option('-p', '--port', type=click.INT, default=8080, help='port of the server')
@click.option('-H', '--api-host', type=click.STRING, default='127.0.0.1', help='IP address of the server')
@click.option('-P', '--api-port', type=click.INT, default=5000, help='port of the server')
def run_api_server(host, port, api_host, api_port):
    """ Listen on HOST:PORT and serve data from API_HOST:API_PORT"""
    try:
        gui.run_server(host, port, api_host, api_port)
    except Exception as error:
        print(f'Error during run_api_server command: {error}')
        return 1


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        click.echo(f'ERROR: {err}')
        sys.exit(1)
