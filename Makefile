#
# Make for pydatomic
#

HIDE ?= @
VENV ?= env
VENV3 ?= env3

all:

test: test-unit test-flake8

test-unit:
	$(HIDE)$(VENV)/bin/nosetests tests

test-flake8:
	$(HIDE)$(VENV)/bin/flake8 --config=tests/flake8.rc pydatomic
	$(HIDE)$(VENV3)/bin/flake8 --config=tests/flake8.rc pydatomic

coverage:
	$(HIDE)$(VENV)/bin/nosetests --with-coverage --cover-erase --cover-inclusive --cover-package=pydatomic pydatomic tests

prepare-venv:
	$(HIDE)virtualenv $(VENV)
	$(HIDE)$(VENV)/bin/pip install --upgrade -r requirements.txt
	$(HIDE)virtualenv --python /usr/bin/python3.4 $(VENV3)
	$(HIDE)$(VENV3)/bin/pip install --upgrade -r requirements.txt
