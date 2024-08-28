.PHONY: all bigbang birth apply init-module create-application

all:
	@echo "Specify a command to run"

init:
	python3 -m venv .venv; \
	until [ -f .venv/bin/python3 ]; do sleep 1; done; \
	until [ -f .venv/bin/activate ]; do sleep 1; done;
	. .venv/bin/activate; \
	pip install PyYAML xia-framework keyring setuptools wheel; \
    pip install keyrings.google-artifactregistry-auth; \

plan: init
	@. .venv/bin/activate; \
	python -m xia_framework.foundation plan

apply: init
	@. .venv/bin/activate; \
	python -m xia_framework.foundation apply

init-module: init
	@if [ -z "$(module_class)" ] || [ -z "$(package)" ]; then \
		echo "Module name not specified. Usage: make init-module module_class=<module_class> package=<package>"; \
	else \
		python main.py init-module -m $(module_class) -p $(package); \
	fi

create-app: init
	@if [ -z "$(app_name)" ]; then \
		echo "Application name not specified. Usage: make create-app app_name=<app_name>"; \
	else \
		python main.py create-app $(app_name); \
	fi