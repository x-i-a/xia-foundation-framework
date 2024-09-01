.PHONY: all init plan apply destroy init-module activate-module

modules ?= ""

all:
	@echo "Specify a command to run"

init:
	python3 -m venv .venv; \
	until [ -f .venv/bin/python3 ]; do sleep 1; done; \
	until [ -f .venv/bin/activate ]; do sleep 1; done;
	. .venv/bin/activate; \
    pip install git+https://github.com/x-i-a/xia-framework.git; \
	pip install PyYAML keyring setuptools wheel; \
    pip install keyrings.google-artifactregistry-auth; \

plan: init
	@. .venv/bin/activate; \
	python -m xia_framework.foundation plan

apply: init
	@. .venv/bin/activate; \
	python -m xia_framework.foundation apply

destroy: init
	@. .venv/bin/activate; \
	python -m xia_framework.foundation destroy

init-module: init
	@. .venv/bin/activate; \
	if [ -z "$(module_uri)" ] ; then \
		echo "Module URI not specified. Usage: make init-module module_uri=<package_name>@<version>/<module_name>"; \
	else \
		python -m xia_framework.foundation init-module -n $(module_uri); \
	fi

activate-module: init
	@. .venv/bin/activate; \
	if [ -z "$(module_uri)" ] ; then \
		echo "Module URI not specified. Usage: make activate-module module_uri=<package_name>@<version>/<module_name>"; \
	else \
		python -m xia_framework.foundation activate-module -n $(module_uri); \
	fi

create-app: init
	@. .venv/bin/activate; \
	if [ -z "$(app_name)" ] ; then \
		echo 'App Name not specified. Usage: make create-app app_name=<app_name> modules="<module1>,<module2>"'; \
	else \
		python -m xia_framework.foundation create-app -n $(app_name) -m $(modules); \
	fi