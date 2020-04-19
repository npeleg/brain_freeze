import importlib
import pathlib
import sys


class Parsers:
    def __init__(self):
        self.parsers = {}
        Parsers.load_parsers('.')

    def get_fields(self):  # TODO re-implement according to load_parsers
        return self.supported_fields.keys()

    @classmethod
    def load_parsers(cls, parsers_dir):
        parsers_dir = pathlib.Path(parsers_dir).absolute()
        sys.path.insert(0, str(parsers_dir.parent))
        for path in parsers_dir.iterdir():
            if path.name.startswith('_') or not path.suffix == ".py":
                continue
            importlib.import_module(f'{parsers_dir.name}.{path.stem}', package=parsers_dir.name)

    def parse_fields(self, context, snapshot):
        for field in self.supported_fields:
            self.supported_fields[field](context, snapshot)


class Context:
    def __init__(self, dir):
        self.dir = dir

    def save(self, filename, contents):
        pathlib.Path(self.dir).mkdir(parents=True, exist_ok=True)
        with open(self.dir / filename, 'w') as file:
            file.write(contents)