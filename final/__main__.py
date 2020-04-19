import click
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import final


@click.group()
def main():
    pass


@main.command('run_webserver')
@click.argument('address', type=click.STRING)
@click.argument('data_dir', type=click.STRING)
def web_run_webserver(address, data_dir):
    try:
        ip, port = address.split(':')
        final.run_webserver((ip, int(port)), data_dir)
    except Exception as error:
        print(f'Error: {error}')
        return 1


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        click.echo(f'ERROR: {err}')
        sys.exit(1)
