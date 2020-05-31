import logging


def get_module_name(name):
    dot_index = name.rindex('.')
    if dot_index != -1:
        return name[dot_index + 1:]
    return name


class Logger:
    def __init__(self, name):
        module_name = get_module_name(name)
        self.logger = logging.getLogger(module_name)  # use only
        self.logger.setLevel(logging.DEBUG)
        cwd = name.replace('.', '/')
        file_handler = logging.FileHandler(f'{cwd}.log')
        formatter = logging.Formatter('%(asctime)s : %(name)s : %(message)s')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
