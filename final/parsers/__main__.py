import click
import sys
from .parsers_logic import Parsers


@click.group()
def main():
    pass


@main.command('parse')
@click.argument('parser_name', type=click.STRING)
@click.argument('source_file', type=click.STRING)
@click.option('dest_file', type=click.STRING, default=None, help='file in which the parsed is stored')
def client_upload_sample(parser_name, source_file, dest_file):
    """ Applies PARSER_NAME parser on DATA_FILE snapshots from file in PATH to server. """
    try:
        result = Parsers().parse(parser_name, source_file)
        if dest_file is None:
            print(result)
        else:
            with open(dest_file, 'w') as file:
                file.write(result)
    except Exception as error:
        print(f'Error during parse command: {error}')
        return 1


@main.command('run_parser') # TODO with - or _ ?
@click.argument('parser_name', type=click.STRING)
@click.argument('url', type=click.STRING)
def client_upload_sample(parser_name, url):
    """ Subscribes PARSER_NAME parser to the 'incoming' topic of the message queue. """
    try:
        pass  # TODO implement
    except Exception as error:
        print(f'Error during parse command: {error}')
        return 1


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        click.echo(f'ERROR: {err}')
        sys.exit(1)
