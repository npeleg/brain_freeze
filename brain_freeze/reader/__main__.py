import click
import sys
from .reader import Reader
from ..utils import protocol


@click.group()
def main():
    pass


@main.command('read')
@click.argument('path', type=click.STRING)
def read_sample(path):
    """ Reads the sample binary file from PATH and prints its data. """
    try:
        reader = Reader(path)
        print(f"User details:\n{protocol.repr_protocol_user(reader.user)}")
        print("Snapshots:\n")
        for snapshot in reader:
            print(protocol.repr_protocol_snapshot(snapshot))
    except Exception as error:
        print(f'Error: {error}')
        return 1


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        click.echo(f'ERROR: {err}')
        sys.exit(1)
