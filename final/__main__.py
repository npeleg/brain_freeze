import sys
import click
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import final


@click.group()
def main():
    pass


@main.command('read')
@click.argument('path', type=click.STRING)
def read_sample(path):
    try:
        reader = final.Reader(path)
        print(f"printing user details:\n{reader.user}")
        print("printing snapshots:\n")
        for snapshot in reader:
            print(snapshot)
    except Exception as error:
        print(f'Error: {error}')
        return 1


@main.command('upload_sample')
@click.argument('host', type=click.STRING)
@click.argument('port', type=click.INT)
@click.argument('path', type=click.STRING)
def client_upload_sample(host, port, path):
    try:
        final.upload_sample((host, int(port)), path)
        print('done.')
    except Exception as error:
        print(f'Error: {error}')
        return 1


@main.command('run_server')
@click.argument('host', type=click.STRING)
@click.argument('port', type=click.INT)
@click.argument('data_dir', type=click.STRING)
def server_run_server(host, port, data_dir):
    try:
        final.server.run_server((host, int(port)), data_dir)
    except Exception as error:
        print(f'Error: {error}')
        return 1


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
