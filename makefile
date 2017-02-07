#!/usr/bin/make -f

# force use of Bash
SHELL := /bin/bash
INTERACTIVE=true
NPM=$$HOME/.nvm/versions/node/v4.4.7/bin/npm

test_daemon_api:
	. ./env/bin/activate \
	&& cd ./daemon/api/ \
	&& python -m unittest discover --verbose

test_daemon_frontend:
	cd ./daemon/frontend/ \
	&& ${NPM} test

test_daemon_core:
	docker exec -it coaxisopt_daemon bats /test/makefile.tests.bats

test_backend_api:
	. ./env/bin/activate \
	&& cd ./backend/api/ \
	&& python -m unittest discover --verbose

test: test_daemon_api test_daemon_frontend test_backend

build_daemon_frontend: test_daemon_frontend
	cd daemon/frontend/ \
	&& ${NPM} run build

deploy: build_daemon_frontend
	cd deploy \
	&& ./build_and_push.sh \
	&& ./send-scripts.sh

connect:
	ssh -F $$HOME/.ssh/config coaxis@opt-forward cd coaxisopt/ -vvv

feature:
	cd daemon/frontend \
	&& bumped release feature

patch:
	cd daemon/frontend \
	&& bumped release patch
