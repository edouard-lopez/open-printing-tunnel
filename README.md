# MAST

**MAST** is a project to setup a Linux service to mount __Multiple Auto-SSH Tunnels__

[TOC]


## Glossary

* **infrastructure**: a machine that manage the customer's tunnels. Can manage multiple customers ;
* **customer**: company that require our service. Can have one or more _hosts_ ;
* **host**: a machine accessible through Internet by its IP address or FQDN. Can have one or more _tunnels_ ;
* **tunnel**: an SSH's tunnel between our infrastructure and the host's machine. Can have one or more channels (each for a different printer);
* **channel**: a port forwarding configuration from _infrastructure_ to _host_ through a _tunnel_.

## Requirements

The first requirement is to have a **Debian-based** system, other distribution are not targeted by this solution. Second you must **create a user called `coaxis`** (as defined by the variable `REMOTE_USER` in the _makefile_).
Others required packages are _automatically installed_ by the `make requirements` command. For reference, here is a list of the main requirements:

* Debian `6.0+` or Ubuntu-server `12.04+` ;
* **GNU `make`**: task manager used to install client/server, deploy add others stuff ;
* `bash` `≥4.x`: the shell interpreter used for the service ;
* `autoSSH`: to start and monitor ssh tunnels ;
	* `openssh-client`: this is an obvious dependency ;
* `trickle`: user-space bandwidth shaper.

Except for _make_, all this dependencies can be [checked](./docs/DAEMON.md#check-system) and [installed](./docs/DAEMON.md#install-requirements) using the makefile, as described below.

## Architecture design: Separation of Concerns

### Service

The core features (_start_, _stop_, _status_, _restart_) are provided through the service file placed in _/etc/mast_

### Administrative Toolbox

All administrative tasks are accomplished through an utility command-line call `mast-utils` placed in _/usr/bin/mast-utils_. A list of available tasks is available in the section [Toolbox's Tasks](./docs/DAEMON.md#toolboxs-tasks).

### Web Interface

Build on top of both the service and the utility toolbox


## Documentation

* [Troubleshooting](docs/TROUBLESHOOTING.md) ;
* [how to docker](docs/HOW-TO-DOCKER.md) ;
* [daemon usage](./daemon/) ;

## Develop

* [Setup Django Backend](backend/README.md)