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

default: build dev

dev:
	${DOCKER_COMPOSE} up -d

rebuild: build
build: remove
	${DOCKER_COMPOSE} build

remove:
	${DOCKER_COMPOSE} rm --force coaxisopt_daemon || true

restart: remove dev

prod:
	docker run -p 80:80 coaxisopt_daemon:latest

install: install-dependencies install-python-requirements

install-dependencies:
	apt install --yes --no-install-recommends --no-install-suggests \
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

test-api:
	source env/bin/activate
	cd api/ && python3 -m unittest discover --verbose

test-api-in-docker:
	docker run \
		--name coaxis-daemon-tests \
		--rm \
		--interactive \
		--tty \
		coaxisopt_daemon \
			bash -c 'service ssh start && cd /api/ && python3 -m unittest discover --verbose'
