#!/usr/bin/env bash

rm -rf dist build
python setup.py sdist
python setup.py bdist_wheel --python-tag py3
twine upload dist/*