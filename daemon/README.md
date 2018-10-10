# OPT Daemon

## Features

* monter les tunnel par `autossh` limité individuellement en bande passante par `trickle` ;
* l'ensemble des tunnels `SSH` présent dans les fichiers de conf doivent tous monter au démarrage de la machine sans intervention humaine ;
* chaque tunnel sera indépendamment, maintenu et logué par le service ;
* chaque tunnel doit pouvoir être monté ou arrêté manuellement ;
* une liste et l'état des tunnel doit être consultable a la demande (service status) ;
* les logs seront séparé par tunnel ;
* le code sera ouvert et documenté ;
* l'ensemble devra être packagé pour une mise en place facile.

## Installation

Building the container will install the requirement. If you want **more details refer to the [Dockerfile](Dockerfile)**.

## Usage

**Note:** direct usage isn't recommended, use the web interface instead.

Options and examples are available in [docs/how-to-use-daemon.md](./docs/how-to-use-daemon.md).

## Test

Note: see `makefile` in root project.

### API

**requirements**: 
There is end-to-end test on this directory to test network methods, you will need to install

    make -f help-me.mk install-dependencies

Then

    make -f help-me.mk test-api

### Frontend

    cd frontend
    npm run test

### Daemon

From host machine we run the tests in a [`bats`](https://github.com/sstephenson/bats) (Bash Automated Testing System) container:

    docker exec -it coaxisopt_daemon_* bats /test/makefile.tests.bats

From inside the container:

    bats test/makefile.tests.bats
        

