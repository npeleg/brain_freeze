import click
import sys
from .saver import Saver


@click.group()
def main():
    pass


@main.command('save')
@click.option('-d', '--database', type=click.STRING, default='postgresql://127.0.0.1:5432',
              help='Database in which the data is stored')
@click.argument('parser_name', type=click.STRING)
@click.argument('source_file', type=click.STRING)
def save(database, parser_name, source_file):
    """ Saves the result of PARSER_NAME found in SOURCE_FILE to a database. """
    try:
        with open(source_file, 'r') as file:
            result = file.read()
        saver = Saver(database)
        saver.save(parser_name, result)
    except Exception as error:
        print(f'Error during save command: {error}')
        return 1


@main.command('run-saver')
@click.argument('database', type=click.STRING)
@click.argument('message_queue', type=click.STRING)
def run_saver(database, message_queue):
    """ Subscribes the saver to messages from MESSAGE_QUEUE and saves them to DATABASE. """
    try:
        Saver(database).run_saver(message_queue)
    except Exception as error:
        print(f'Error during run_saver command: {error}')
        return 1


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        click.echo(f'ERROR: {err}')
        sys.exit(1)
