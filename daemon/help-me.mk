#!/usr/bin/make -f
# DESCRIPTION
#	Help you setup the env to work locally
#
# USAGE
#	make -f help-me.mk
#   or
#	make -f help-me.mk test-backend


# force use of Bash
SHELL := /bin/bash
DOCKER_COMPOSE=docker-compose -f docker-compose.dev.yml

default: build dev

dev:
	${DOCKER_COMPOSE} up -d
	echo 'Visit: http://localhost/'

rebuild: build
build: remove
	${DOCKER_COMPOSE} build --pull

remove:
	${DOCKER_COMPOSE} rm --force coaxisopt_daemon || true

restart: remove dev

prod:
	docker run -p 80:80 coaxisopt_daemon:latest

install: install-dependencies install-python-requirements

install-dependencies:
	sudo apt-get install --yes --no-install-recommends --no-install-suggests \
			autossh \
			dpkg \
			gawk \
			fping \
			grep \
			htop \
			libsmi2-dev \
			libffi-dev \
			libc-bin \
			make \
			nano \
			nmap \
			openssh-server \
			openssh-client \
			snmp \
			snmpd \
			snmp-mibs-downloader \
			sshpass \
			sudo \
			trickle \
			vim-tiny \
			wget \
			whois \
			ca-certificates \
			nginx \
			supervisor 

install-python-requirements:
	echo  'create virtual env in daemon/'
	cd ..
	python3 -m venv env
	source env/bin/activate \
	&& pip3 install -r requirements.txt

test-backend: build
	docker run \
		--name test-coaxis-backend \
		--rm \
		--interactive \
		--env IN_DOCKER=true \
		coaxisopt_daemon \
			bash -c 'service ssh start && cd /api/ && python3 -m unittest discover --verbose --failfast'

test-backend-dev: dev
	echo 'Mount source code in container'
	docker exec \
		--interactive \
		--env IN_DOCKER=true \
		coaxisopt_daemon \
			bash -c 'service ssh start && cd /api/ && python3 -m unittest discover --verbose --failfast '

test-frontend-unittest:
	cd ./frontend/ \
	&& yarn test

API_READY:=curl --write-out "%{http_code}" http://localhost/ | grep 200
test-frontend-end-to-end: dev 
	while ! ${DOCKER_COMPOSE} exec -T daemon sh -c '${API_READY}'; do sleep .1s; done
	cd ./frontend/ \
	&& yarn test:e2e

test-mast:
	docker run \
		--name test-coaxis-mast \
		--rm \
		--interactive \
		coaxisopt_daemon bash -c 'bats /test/*.tests.bats'
