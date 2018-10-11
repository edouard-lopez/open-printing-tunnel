#!/usr/bin/make -f

# force use of Bash
SHELL := /bin/bash
INTERACTIVE=true

test-daemon-api:
	cd daemon/ \
	&& make -f help-me.mk test-api

test-daemon-frontend:
	cd daemon/ \
	&& make -f help-me.mk test-frontend

test-daemon-core:
	cd daemon/ \
	&& make -f help-me.mk test-core

test-backoffice-api:
	cd backend/ \
	&& make test-api

test-backoffice-frontend:
	cd ./frontend/ \
	&& npm test

tests: test-daemon-api test-daemon-frontend test-daemon-core test-backoffice-api test-backoffice-frontend

build-daemon-frontend: test-daemon-frontend
	cd daemon/frontend/ \
	&& npm run build

deploy: build-daemon-frontend
	cd deploy \
	&& ./build_and_push.sh \
	&& ./send-scripts.sh

connect:
	ssh -F $$HOME/.ssh/config coaxis@opt-forward cd coaxisopt/ -vvv

tag-as-feature:
	cd daemon/frontend \
	&& bumped release feature

tag-as-patch:
	cd daemon/frontend \
	&& bumped release patch
