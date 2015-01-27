#
# Make for pydatomic
#

HIDE ?= @
VENV ?= env

all:

test:
	$(HIDE)$(VENV)/bin/nosetests tests

prepare-venv:
	$(HIDE)virtualenv $(VENV)
	$(HIDE)$(VENV)/bin/pip install --upgrade -r requirements.txt
