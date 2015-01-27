#
# Make for pydatomic
#

HIDE ?= @
VENV ?= env

all:

test:
	$(HIDE)$(VENV)/bin/nosetests tests

coverage:
	$(HIDE)$(VENV)/bin/nosetests --with-coverage --cover-erase --cover-inclusive --cover-package=pydatomic pydatomic tests

prepare-venv:
	$(HIDE)virtualenv $(VENV)
	$(HIDE)$(VENV)/bin/pip install --upgrade -r requirements.txt
