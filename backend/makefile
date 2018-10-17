#!/usr/bin/make -f
# DESCRIPTION
#	Help you setup the env to work locally
#
# USAGE
#	make -f help-me.mk
#   or
#	make -f help-me.mk test-api


# force use of Bash
SHELL := /bin/bash
DOCKER_COMPOSE=docker-compose -f docker-compose.dev.yml

default: install

install: install-python-requirements

install-python-requirements:
	python3 -m venv env
	source env/bin/activate \
	&& pip3 install -r requirements.txt

reset-test-env:
	docker stop --time 0 $$(docker ps | awk '/coaxisopt_daemon/ {print $$1}') || true
	docker network prune --force
	docker rm --force $$(docker ps | awk '/coaxisopt_daemon/ {print $$1}') || true

test-api: reset-test-env
	source env/bin/activate \
	&& export DEFAULT_INTERFACE=wlp4s0 \
	&& ./manage.py test -v 2
