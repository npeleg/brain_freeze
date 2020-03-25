from setuptools import setup, find_packages


setup(
    name = 'asdF',
    version = '0.1.0',
    author = 'Peleg Neufeld',
    description = 'An example package.',
    packages = find_packages(),
    install_requires = ['click'],
    tests_require = ['pytest'],
)
