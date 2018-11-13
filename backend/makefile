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
DEFAULT_INTERFACE:=wlp4s0


default: install

install: install-python-requirements

install-python-requirements:
	python3 -m venv env
	source env/bin/activate \
	&& pip3 install -r requirements.txt

COAXIS_CONTAINERS:=docker ps --all | awk '/coaxisopt_daemon/ {print $$1}'
COAXIS_CONTAINERS_EXIST:=(( $$(${COAXIS_CONTAINERS} | wc --lines) > 0 ))
reset-test-env:
	if ${COAXIS_CONTAINERS_EXIST}; then docker stop --time 0 $$(${COAXIS_CONTAINERS}); fi
	docker network prune --force
	if ${COAXIS_CONTAINERS_EXIST}; then docker rm --force $$(${COAXIS_CONTAINERS}); fi

test-api: reset-test-env
	source env/bin/activate \
	&& export DEFAULT_INTERFACE=${DEFAULT_INTERFACE} \
	&& ./manage.py test --failfast --verbosity 2
