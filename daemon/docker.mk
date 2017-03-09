#!/usr/bin/make -f
# DESCRIPTION
#	Tiny utility to build and run the local container
#
# USAGE
#	./docker.mk
#   or
#	./docker.mk build
#	then
#	./docker.mk dev


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

test:
    echo "see <root>/makefile"