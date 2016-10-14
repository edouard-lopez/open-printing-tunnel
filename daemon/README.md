# OPT daemon

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

This is done during the docker container building process, if you want **more details refer to the [Dockerfile](Dockerfile)**.


## Test

### Requirements

* [`bats`](https://github.com/sstephenson/bats) (Bash Automated Testing System).

### Run

From host machine:

    docker exec -it coaxisopt_daemon bats /test/makefile.tests.bats

From inside the container:

    bats test/makefile.tests.bats
        

## Toolbox's Tasks

A _makefile_ define so-called _tasks_, that allow admin to easily run a complex sequence of commands in a single call. For instance, `make install` might run commands to ① [check the system state](#check-system), ② [install the requirements](#install-requirements), ③ [configure everything](#deploying), etc.

It is useful to know that a `make` command can take a series of tasks to accomplish, the previous `make install` task could have been run as `make check-system requirements deploy`, which is more explicit but a bit longer.

### Tips and Tricks

For administrator familiar with _Bash_'s syntax but unfamiliar with `makefile`'s one, you need to be aware of the following:

* variables can be pass to the makefile script as follow: `make MYVAR=123 taskname` ;
* the `$` (dollar sign) **must be escaped** if you want to have access to bash variable (e.g. ~~$HOME~~ → `$$HOME`) ;
* multi-lines Bash commands should end with a `; \` (semi-column and backslash). Otherwise _make_ will consider each line to be isolated for the surrounding ones ;
* the `@` (at sign) in the begin of a line is use to prevent a command to be printed prior to execution. If you want to see what commands the task really executed, with variables expanded, simply remote the `@`-sign from the beginning of the line :).

### Default Usage (alias)

Aliases to [Usage](#usage).

```bash
sudo make
```

## Modules Deployment

### Deploy

This task is now done by the [daemon's `Dockerfile`](../Dockerfile).

### Install

This is a meta-task that will run the following dependencies:

* [Install project dependencies](#install-requirements) ;
* [Check system](#check-system) and [privileges](](#check-privileges)) ;
* [Deploy the service and webapp](#deploy) ;
* [Create a SSH key pair](#create-ssh-key) if necessary.

```bash
sudo make install
```
![sudo-make-install](./screenshots/installation-02-make-install.png)

### Install Requirements

Install required packages (`autossh`, `trickle`, `openssh-client`, ...) on the infrastructure.

```bash
sudo make setup-infra
```
![sudo-make-requirements](./screenshots/sudo-make-requirements.png)

## SSH Key
### Create SSH Key (alias)

Aliases to [${SSH_KEYFILE}](#ssh_keyfile).

Create SSH keys pair on infrastructure to allow friction-less connection to the customer's node.

```bash
make create-ssh-key
```
![sudo-make-create-ssh-key](./screenshots/sudo-make-create-ssh-key.png)

### `${SSH_KEYFILE}`

Aliased by [Create SSH Key](#create-ssh-key-alias).

### Deploy Key

Copy infra public key on customer's node, as defined by `REMOTE_HOST`.

Once the ssh keys are created we need to copy the public key on the (remote) customer's node, in order to leverage authentication mechanism.

**Warning:** must be **run as normal user** to prevent permissions issues.

![make-deploy-key](./screenshots/sudo-make-deploy-key.png)

```bash
make deploy-key
```

If the customer's node address differ from the default value `REMOTE_HOST` (see in the _makefile_), the new value must be passed **as an argument**, as follow:

```bash
make REMOTE_HOST=11.22.33.44 deploy-key
```

### Config SSH (alias)

Aliases to [Deploy Key](#deploy-key).

## Hosts management
### List Hosts
List all hosts available to the service.
```bash
sudo make list-hosts
```
![sudo-make-list-logs](./screenshots/sudo-make-list-hosts.png)

### Add Host

Adding a new host configuration. Both `NAME` **and** `REMOTE_HOST` are required.

| Parameter  | Default | Description |
| ------------- | ------------- | ------------- |
| `NAME` | **required** | **_string_**. Configuration name. |
| `REMOTE_HOST` | **required** | **_string_**. Host IP address or FQDN. |

Example:
```bash
sudo make add-host REMOTE_HOST=1.1.1.1 NAME=nautilus
```
![sudo-make-add-host](./screenshots/sudo-make-add-host.png)

### Remove Host
Remove an host by name. For instance, to remove the _second_ channel from the client _nautilus_

| Parameter  | Default | Description |
| ------------- | ------------- | ------------- |
| `NAME` | **required** | **_string_**. Configuration name. |

```bash
sudo make remove-host NAME=nautilus
```
![sudo-make-remove-host](./screenshots/sudo-make-remove-host.png)

### Check Privileges

Check files permission.

![sudo-make-check-privileges](./screenshots/sudo-make-check-privileges.png)

### Check System
Check system status for dependencies.

After getting the project source code, you can check your system status for requirements using :

```bash
make check-system
```
Once the system is ready for the service, you should get the following output:
![dependencies.(./screenshots/sudo-make-check-system](./screenshots/sudo-make-check-system.png)

## Channels management

### List Channels
List channels for given host. if none is given, iterate over all hosts.

| Parameter  | Default | Description |
| ------------- | ------------- | ------------- |
| `NAME` | _optional_ | **_string_**. Configuration name. |

```bash
sudo make list-channels
# or
sudo make list-channels NAME=nautilus
```

### Add Channel

Add a new channel for the given printer.

| Parameter  | Default | Description |
| ------------- | ------------- | ------------- |
| `NAME` | **required** | **_string_**. Configuration name. |
| `PRINTER` | **required** | **_string_**. Printer's hostname or ip. |
| `DESC` | _optional_ | **_string_**. Description/comment of the channel. |

Example:
```bash
make add-channel NAME=nautilus PRINTER=1.1.1.1 DESC="Comment blabla"
```
![sudo-make-add-channel](./screenshots/sudo-make-add-channel.png)

### Remove Channel

Remove a channel using its index position from a given host.

| Parameter  | Default | Description |
| ------------- | ------------- | ------------- |
| `ID` | **required** | **_integer_**. channel index as given by `sudo make list-channels` (cf. [List Channels](#list-channels). |
| `NAME` | **required** | **_string_**. Configuration name. |


For instance, to remove the _second_ channel from the client _nautilus_
```bash
sudo make remove-channel ID=2 NAME=nautilus
```
![sudo-make-remove-channel](./screenshots/sudo-make-remove-channel.png)

## Helper
### Usage
Display basic help. for further information refer to the [official docs](http//github.com/edouard lopez/mast/readme.md).
![sudo-make-usage](./screenshots/sudo-make-usage.png)

### Uninstall

Remove configuration files, services, utility, etc. So you can make a fresh [install](#install).
![sudo-make-uninstall](./screenshots/sudo-make-uninstall.png)

### List Logs
List all log files, one for each tunnel.
```bash
sudo make list-logs
```
![sudo-make-list-logs](./screenshots/sudo-make-list-logs.png)

## Service

### Don't kill me, I have kids!

Check if tunnels are children of the service. If this is the case, that means that killing the service will kill **all** tunnels.

## Configuration File

The configuration files used by `mast` are located in the `$CONFIG_DIR` directory as defined in the _makefile_ (default path is `/etc/mast/`).
Those files are dynamically generated using the `make add-host` and use the _template_ file as skeleton. Each configuration describe parameters for a given host and most configuration should not be tampered with.

Below is a list of available parameters and their roles:

| Parameter  | Default | Description |
| ------------- | ------------- | ------------- |
| `RemoteHost` | _HOST_ | **_string_**. [FQDN](https://en.wikipedia.org/wiki/FQDN) or IP address of the customer's node.. |
| `RemoteUser` | _coaxis_ | **_string_**. Unix' username on the customer's node.. |
| `RemotePort` | `22` | **_integer_**. SSH port on the customer's node.. |
| `ServerAliveInterval` | `10` | **_integer_**. Sets a timeout interval in seconds[^manpage-ssh-config] after which if no data has been received from the server, `ssh` will send a message through the encrypted channel to request a response from the server.. |
| `ServerAliveCountMax` | `3` | **_integer_**. Sets the number of server alive messages which may be sent without `ssh` receiving any messages back from the server.[^manpage-ssh-config]. |
| `StrictHostKeyChecking` | _no_ | **_string_**. If this flag is set to _no_, `ssh` will automatically add new host keys to the user known hosts files.[^manpage-ssh-config]. |
| `LocalUser` | _mast_ | **_string_**. The user on the local machine that will be used to create the tunnel.[^js-morisset]. |
| `IdentityFile` | _/home/$LocalUser/.ssh/<br/>id_rsa.mast.coaxis.pub_ | **_string_**. Path to local SSH public key, so we can connect automatically to customer's node.. |
| `ForwardPort` | `"L *:9100:imp1:9100"``"L *:9101:imp2:9100"` | **_array_**.`L [bind_address:]port:host:hostport` Specifies that the given port on the local (client) host is to be forwarded to the given host and port on the remote side.`R [bind_address:]port:host:hostport` Specifies that the given port on the remote (server) host is to be forwarded to the given host and port on the local side.. |
| `BandwidthLimitation` | `true` | **_boolean_**. Flag to toggle  traffic limitation.`true`: enable limitation or `false`: disable.. |
| `UploadLimit` | `1000` | **_integer_**. Upper limit for _upload_ traffic (customer's node is the source of traffic).. |
| `DownloadLimit` |`100` | **_integer_**. Upper limit for _download_ traffic.. |

### References

* [^manpage-ssh-config]: [Manual for OpenSSH SSH **client configuration files**.](http://manpages.ubuntu.com/manpages/precise/en/man5/ssh_config.5.html)
* [^js-morisset]: [Autossh Startup Script for Multiple Tunnels.](http://surniaulula.com/2012/12/10/autossh-startup-script-for-multiple-tunnels/)
* [^manpage-ssh-client]: [Manual for OpenSSH SSH **client**.](http://manpages.ubuntu.com/manpages/precise/en/man1/ssh.1.html)
