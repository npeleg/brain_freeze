import importlib
import pathlib
import sys
from ..utils import Logger, MQManager

logger = Logger(__name__).logger


def load_parsers(parsers_dir, parsers_dict):
    """ Dynamically imports all the parsers in parsers_dir and inserts them to a dictionary"""
    abs_parsers_dir = pathlib.Path(parsers_dir).absolute()
    sys.path.insert(0, str(abs_parsers_dir.parent))
    logger.info('loading parser modules')
    for path in abs_parsers_dir.iterdir():
        if path.name.startswith('_') or not path.suffix == ".py":
            continue
        module = importlib.import_module(f'{abs_parsers_dir.name}.{path.stem}', package=abs_parsers_dir.name)
        parse_func = getattr(module, 'parse')
        parsers_dict[module.parse.name] = parse_func


def wrap_parser(parser_name, parser_func, mq):
    """ returns a function that parses data using parser_func and publishes the result to the parser_name topic"""
    def parse_and_publish(data):
        parsed_data = parser_func(data)
        logger.info('parsed data is: ' + parsed_data)
        mq.publish_to_topic(parser_name, parsed_data)
    return parse_and_publish


class Parsers:
    def __init__(self):
        self.parsers_dict = {}
        load_parsers('./final/parsers/parsers', self.parsers_dict)

    def get_parsers_names(self):
        """ Return the parsers' names """
        logger.info('sending parsers names')
        return self.parsers_dict.keys()

    def parse(self, parser_name, data):
        return self.parsers_dict[parser_name](data)

    def run_parser(self, parser_name, mq_url):
        if parser_name not in self.parsers_dict:
            raise KeyError("parser does not exist")
        parser = self.parsers_dict[parser_name]
        mq = MQManager(mq_url)
        logger.info(f'adding a topic for the parsed results of {parser_name} parser')
        mq.create_topic(parser_name)
        mq.create_incoming_topic()
        logger.info(f'subscribing {parser_name} parser to incoming topic')
        parse_and_publish = wrap_parser(parser_name, parser, mq)
        mq.subscribe_to_incoming_topic(parse_and_publish)
