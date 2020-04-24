import importlib
import pathlib
import sys


def load_parsers(parsers_dir):
    """ Dynamically imports all the parsers in parsers_dir and inserts them to a dictionary"""
    parsers_dir = pathlib.Path(parsers_dir).absolute()
    sys.path.insert(0, str(parsers_dir.parent))
    for path in parsers_dir.iterdir():
        if path.name.startswith('_') or not path.suffix == ".py":
            continue
        importlib.import_module(f'{parsers_dir.name}.{path.stem}', package=parsers_dir.name)


class Parsers:
    def __init__(self):
        self.parsers_dict = {}
        # Parsers.load_parsers('.')

    def get_parsers_names(self):
        """Return the parsers' names (used to construct a protocol Config message)"""
        return self.parsers_dict.keys()

    def parse(self, field, data):
        return self.parsers_dict[field]
