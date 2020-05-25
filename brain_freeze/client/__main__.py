import click
import sys
from .client import upload_sample


@click.group()
def main():
    pass


@main.command('upload_sample')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1', help='IP address of the server')
@click.option('-p', '--port', type=click.INT, default=8000, help='port of the server')
@click.argument('path', type=click.STRING)
def client_upload_sample(host, port, path):
    """ Upload snapshots from file in PATH to server. """
    try:
        upload_sample(host, int(port), path)
    except Exception as error:
        print(f'Error: {error}')
        return 1


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        click.echo(f'ERROR: {err}')
        sys.exit(1)
