[![Build Status](https://travis-ci.com/npeleg/final.svg?branch=master)](https://travis-ci.com/npeleg/final)
[![codecov](https://codecov.io/gh/npeleg/final/branch/master/graph/badge.svg)](https://codecov.io/gh/npeleg/final)

# BrainFreeze
Welcome to the BrainFreeze project!
Here you will find instructions for installation and basic usage of the project's features.
For the full documentation click here.

BrainFreeze constitutes the software side of a computer-brain interface product.
The product's hardware side constantly produces cognition snapshots of the user, sent to BrainFreeze system for processing and analysis.
A cognition snapshot consists of: 
 - the user's location and head's rotation (combining those forms the user's 'pose')
 - the image that the user saw 
 - the depth image that the user saw (the distance of the nearest object in each point of the user's view)
 - the timestamp the snapshot was taken at
 
To simulate the hardware side, you are supplied with a binary file containing the user's cognition snapshots taken in the morning hours of April 4th, 2019. 
The software side - the BrainFreeze system and its components - is explained below.

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone https://github.com/npeleg/brain_freeze.git 
    ...
    $ cd brain_freeze/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [brain_freeze] $ # that's it!
    ```

3. To check that everything is working as expected, run the tests:

    ```sh
    $ pytest tests/
    ...
    ```

## Usage

The `brain_freeze` package provides the following components:

- `client`

    The client component encapsulates the concept of `foo`, and returns `"foo"` when run.

    In addition, it provides the `inc` method to increment integers, and the
    `add` method to sum them.

    ```pycon
    >>> from foobar import Foo
    >>> foo = Foo()
    >>> foo.run()
    'foo'
    >>> foo.inc(1)
    2
    >>> foo.add(1, 2)
    3
    ```

- `Bar`

    This class encapsulates the concept of `bar`; it's very similar to `Foo`,
    except it returns `"bar"` when run.

    ```pycon
    >>> from foobar import Bar
    >>> bar = Bar()
    >>> bar.run()
    'bar'
    ```

The `foobar` package also provides a command-line interface:

```sh
$ python -m foobar
foobar, version 0.1.0
```

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

The CLI provides the `foo` command, with the `run`, `add` and `inc`
subcommands:

```sh
$ python -m foobar foo run
foo
$ python -m foobar foo inc 1
2
$ python -m foobar foo add 1 2
3
```

The CLI further provides the `bar` command, with the `run` and `error`
subcommands.

Curiously enough, `bar`'s `run` subcommand accepts the `-o` or `--output`
option to write its output to a file rather than the standard output, and the
`-u` or `--uppercase` option to do so in uppercase letters.

```sh
$ python -m foobar bar run
bar
$ python -m foobar bar run -u
BAR
$ python -m foobar bar run -o output.txt
$ cat output.txt
BAR
```

Do note that each command's options should be passed to *that* command, so for
example the `-q` and `-t` options should be passed to `foobar`, not `foo` or
`bar`.

```sh
$ python -m foobar bar run -q # this doesn't work
ERROR: no such option: -q
$ python -m foobar -q bar run # this does work
```

To showcase these options, consider `bar`'s `error` subcommand, which raises an
exception:

```sh
$ python -m foobar bar error
ERROR: something went terribly wrong :[
$ python -m foobar -q bar error # suppress output
$ python -m foobar -t bar error # show full traceback
ERROR: something went terribly wrong :[
Traceback (most recent call last):
    ...
RuntimeError: something went terrible wrong :[
```
