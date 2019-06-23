# Makefile for Gousto Recipe API server

VIRTUALENV_DIR?=./venv
PYTHON_BIN=python3

export PYTHONPATH:=./src:$(PYTHONPATH)

.PHONY: help
help:
	@echo "Gousto Recipe API server"
	@echo "  Available Targets: venv"
	@echo "    venv  - Build python virtual environment"
	@echo "  The following targets require the above venv to already be activated"
	@echo "    test  - Run tests"
	@echo "    run   - Run dev server"

.PHONY: venv
venv:
	virtualenv --python=$(PYTHON_BIN) $(VIRTUALENV_DIR)
	$(VIRTUALENV_DIR)/bin/pip install --upgrade pip
	$(VIRTUALENV_DIR)/bin/pip install -r requirements.txt
	@echo "Activate the new virtual environment with: source $(VIRTUALENV_DIR)"
 
.PHONY: test
test: test-unit test-feature

.PHONY: lint
lint:
	flake8 src tests features

.PHONY: test-features
test-features:
	behave

>PHONY: test-unit
test-unit:
	pytest

.PHONY: run
run:
	python src/app.py
