#!/usr/bin/make -f

# force use of Bash
SHELL := /bin/bash
INTERACTIVE=true

default: dev
 
test-backoffice-backend:
	cd backend/ \
	&& make test-api

test-backoffice-frontend:
	cd ./frontend/ \
	&& npm test

test-backoffice: test-backoffice-backend test-backoffice-frontend


test-mast:
	cd daemon/ \
	&& make -f help-me.mk test-mast

test-frontoffice-backend:
	cd daemon/ \
	&& make -f help-me.mk test-backend

test-frontoffice-frontend:
	cd daemon/ \
	&& make -f help-me.mk test-frontend-unittest

test-frontoffice-end-to-end:
	cd daemon/ \
	&& make -f help-me.mk test-frontend-end-to-end

test-frontoffice: test-mast test-frontoffice-backend test-frontoffice-frontend test-frontoffice-end-to-end


tests: test-backoffice test-frontoffice

connect:
	ssh -F $$HOME/.ssh/config coaxis@opt-forward cd coaxisopt/ -vvv

tag-as-feature:
	cd daemon/frontend \
	&& bumped release feature

tag-as-patch:
	cd daemon/frontend \
	&& bumped release patch

release:
	cd deploy/ \
	&& ./release.sh "$$(git describe --abbrev=0 --tags)"

prepare-env:
	docker-compose build # create the containers images 
	docker-compose up -d # start project

first-run: prepare-env
	docker exec -it coaxisopt_backend bash -c './manage.py createsuperuser'

reset-test-env:
	docker network prune --force

where-is-front-office:
	frontoffice_ip="$$(docker inspect coaxisopt_daemon_1 --format "{{ json .NetworkSettings.Networks.coaxisopt_default.IPAddress }}" | python -m json.tool | sed -s 's/"//g')" \
	&& echo "Front-office → http://$$frontoffice_ip/"
	echo

dev: reset-test-env prepare-env where-is-front-office
	echo "Back-office → http://localhost/"

dev-frontoffice:
	cd daemon/ \
	&& make -f help-me.mk dev

restart-flask:
	docker exec	coaxisopt_daemon bash -c 'supervisorctl restart flask'
