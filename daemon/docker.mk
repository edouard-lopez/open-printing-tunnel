#!/usr/bin/make -f
# DESCRIPTION
#	Tiny utility to build and run the local container
#
# USAGE
#	./docker.mk
#   or
#	./docker.mk build
#	then
#	./docker.mk run


# force use of Bash
SHELL := /bin/bash

default: build run

dev:
	docker run -d \
		--name daemon \
		-p 80:80 \
		-p 8080:8080 \
		-p 5000:5000 \
		-v "$$(pwd)"/api:/api \
		-v "$$(pwd)"/frontend:/frontend \
		-v node_modules:/frontend/node_modules \
		coaxisopt_daemon:latest \
		/usr/bin/supervisord -c /etc/supervisor/conf.d/dev.conf

rebuild: build
build: remove
	docker build -t coaxisopt_daemon ./

remove:
	docker rm --force daemon || true

restart: remove run

prod:
	docker run -p 80:80 coaxisopt_daemon:latest