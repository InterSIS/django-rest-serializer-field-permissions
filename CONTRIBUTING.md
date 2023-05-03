# Contributing

This document contains technical instructions for how to develop this package. See [the readme](README.md) for a description of what kinds of changes might be accepted. 

## Installing Development Requirements

First, create a virtual environment with the version of Python specified in [the tox file](tox.ini).

Then, install the development requirements:

```bash
$ pip install -e .[dev]
```

## Running Tests

Use tox to run tests against all supported versions:

```bash
$ tox
```

## Publishing the Library

Make sure that you've updated the library version in [`setup.py`](setup.py). Then build and publish the library:

```bash
$ python setup.py sdist
$ python -m twine upload dist/*
```