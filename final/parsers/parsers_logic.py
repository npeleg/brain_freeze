import importlib
import pathlib
import sys


class Parsers:
    def __init__(self):
        self.parsers_dict = {}
        Parsers.load_parsers('.')

    @classmethod
    def load_parsers(cls, parsers_dir):
        """ Dynamically imports all the parsers in parsers_dir and inserts them to a dictionary"""
        parsers_dir = pathlib.Path(parsers_dir).absolute()
        sys.path.insert(0, str(parsers_dir.parent))
        for path in parsers_dir.iterdir():
            if path.name.startswith('_') or not path.suffix == ".py":
                continue
            importlib.import_module(f'{parsers_dir.name}.{path.stem}', package=parsers_dir.name)

    def get_parsers_names(self):
        """Return the parsers' names (used to construct a protocol Config message)"""
        return self.parsers_dict.keys()

    def parse_fields(self, context, snapshot):
        for field in self.parsers_dict:
            self.parsers_dict[field](context, snapshot)
