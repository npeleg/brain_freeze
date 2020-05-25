from setuptools import setup, find_packages

setup(
    name='brain_freeze',
    version='0.1.0',
    author='Peleg Neufeld',
    description='Final project for Advanced Systems Design course.',
    packages=find_packages(),
    install_requires=['click'],
    tests_require=['pytest'],
)
