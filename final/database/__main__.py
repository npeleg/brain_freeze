import click
import sys


@click.group()
def main():
    pass

# TODO delete


@main.command('get-users')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1', help='IP address of the server')
@click.option('-p', '--port', type=click.INT, default=5000, help='port of the server')
@click.argument('a')
def get_users(host, port, a):
    print(a)


@main.command('get-users')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1', help='IP address of the server')
@click.option('-p', '--port', type=click.INT, default=5000, help='port of the server')
@click.argument('a')
@click.argument('b')
def get_users(host, port, a, b):
    print(b)


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        click.echo(f'ERROR: {err}')
        sys.exit(1)
