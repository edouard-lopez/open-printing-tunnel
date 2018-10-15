#!/usr/bin/make -sf
# DESCRIPTION
#	Project utility to install client/server, deploy, etc.
#
# USAGE
#	sudo make REMOTE_HOST=255.255.255.255 deploy-key
#
# AUTHOR
#	Édouard Lopez <dev+mast@edouard-lopez.com>

ifneq (,)
This makefile requires GNU Make.
endif


# default remote user
#  /!\ It is assumed ${REMOTE_USER} already exist on system
REMOTE_USER:=coaxis
REMOTE_INIT_PWD:=C1i3ntRmSid3
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# DO NOT EDIT.
# Below are CRITICAL SETTINGS for the application.
# Seriously, otherwise you VOID THE SUPPORT AND WARRANTY contract.

APP:=mast
# group holding web server (default is Apache2f)
WEB_SERVER:=www-data

# force use of Bash
SHELL := /bin/bash
INTERACTIVE=true

# default remote hostname
REMOTE_HOST:=none
# Current customer's name config and host/ip to work with (add/delete)
NAME:=none
PRINTER:=none
# channel description (default: empty).
DESC:=
# channel's id, used for removal
ID:=-1

# SSH tunnel configuration directory (a file per host)
CONFIG_DIR:=/etc/mast
# Log files directory
LOG_DIR:=/var/log/mast
# Pid files directory for the service
PID_DIR=/var/run/${APP}
# Lock files directory for the service
LOCK_DIR=/var/lock/${APP}

# Passphrase MUST be empty to allow automation (no passphrase prompt)
EMPTY:=
# Path to the SSH keys pair (public key is suffixed by .pub).
SSH_DIR:=/home/${APP}/.ssh
SSH_KEYFILE:=${SSH_DIR}/id_rsa.mast.coaxis

# webapp sources directory, cloned during install (deployed to /var/www/${WEBAPP})
WEBAPP=webapp
# location of served web app.
WEBAPP_DEST_DIR=/var/www/

# Project dependencies
DEPS_CORE_INFRA:=autossh openssh-client trickle apache2 libapache2-mod-php5 sudo aha sshpass whois libc-bin
DEPS_UTILS:=bmon iftop htop

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


.PHONY:  default \
	add-channel \
	add-host  \
	check-privileges  \
	check-system  \
	config-ssh  \
	create-ssh-key  \
	deploy  \
	deploy-key  \
	install  \
	list-channels  \
	list-hosts  \
	list-logs  \
	remove-channel \
	remove-host  \
	usage


default: usage
create-ssh-key: ${SSH_KEYFILE}


# List channels for given host. If none is given, iterate over all hosts
# @optional: {string} NAME host's name
list-channels:
	@# if no config names (on the command-line), stop all autossh processes
	@if [[ -e "${CONFIG_DIR}/${NAME}" ]]; then \
		config=(  "${CONFIG_DIR}/${NAME}" ); \
	else \
		config=( "${CONFIG_DIR}"/* ); \
	fi; \
	for cfg in "$${config[@]}"; do \
		host="$$(basename "$$cfg")"; \
		[[ $$host == "template" ]] && continue; \
		if (( "$${#config[@]}" > 1 )); then \
			remoteHost="$$(grep RemoteHost "$$cfg" | tr -d ' \"' | cut -d '=' -f 2 )"; \
			printf "\t%-50s%s\n" $$'$(call VALUE,'$$host$$')' $$'$(call INFO,'"$$remoteHost"$$')'; \
		fi; \
		source "$${cfg}"; \
		for i in "$${!ForwardPort[@]}"; do \
			rule="$$(echo $${ForwardPort[i]} | awk -F '#' '{print $$1}' | sed -e 's/^ *//' -e 's/ *$$//')"; \
			comment="$$(echo $${ForwardPort[i]} | awk -F '#' '{ $$1=""; print $$0}' | sed -e 's/^ *//' -e 's/ *$$//')"; \
			printf "\t%-45s%-15s\t%s\n" $$'$(call VALUE,'"$$rule"$$')' $$'$(call INFO,'"$$i"$$')' $$'$(call DEBUG,'"# $$comment"$$')'; \
		done; \
	done


# List all log files, one for each tunnel
list-logs:
	@for log in "${LOG_DIR}/${APP}"-*.log; do \
		fn="$$(basename "$$log")"; \
		[[ ! -f $$log || -d $$log || $fn == "template" ]] && continue; \
		printf "\t%-50s%s\n" $$'$(call VALUE,'"$$fn"$$')' $$'$(call INFO,'"$$log"$$')'; \
	done


# List all hosts available to the service
list-hosts:
	@for fn in ${CONFIG_DIR}/*; do \
		h=$$(basename "$$fn"); \
		[[ $$h == "template" ]] && continue; \
		remoteHost="$$(grep RemoteHost "$$fn" | tr -d ' \"' | cut -d '=' -f 2 )"; \
		printf "\t%-50s%s\n" $$'$(call VALUE,'$$h$$')' $$'$(call INFO,'"$$remoteHost"$$')'; \
	done


# Add a new channel for the given printer to the given host
# @require: {string} 	NAME 		configuration name as given to 'add-host'
# @require: {string} 	PRINTER 	printer's hostname or ip
# @option: {string} 	DESC 		description/comment of the channel
add-channel:
	@printf "Adding channel…\n"
	@if [[ ${NAME} == "none" || -z "${NAME}" ]]; then \
		printf "\t%-50s%s\t%s\n" $$'$(call VALUE,NAME)' $$'$(call ERROR,missing)' \
									$$'$(call INFO,(see \'mast-utils list-host\'))'  1>&2; \
		exit 1; \
	fi
	@if [[ "${PRINTER}" == "none" || -z "${PRINTER}" ]]; then \
		printf "\t%-50s%s\t%s\n" $$'$(call VALUE,PRINTER)' $$'$(call ERROR,missing)' \
									$$'$(call INFO,(IP address or hostname))'  1>&2; \
		exit 1; \
	fi

	while ! mkdir /tmp/mast.busy 2> /dev/null; do sleep .1s; done  # waiting for lock to free
	grep --no-filename --only-matching --perl-regexp 'L[\s]+\*:([\d]+):' ${CONFIG_DIR}/* \
		| cut --delimiter=':' -f 2 \
		| sort --unique --numeric-sort \
	> /tmp/ports; \
	prevPort=$$(head -n 1 /tmp/ports); \
	nextPort=$$prevPort;\
	while read -r port; do \
		(( port == nextPort )) && PORT=$$nextPort || break; \
		prevPort=$$port; \
		nextPort=$$(( $$prevPort+1 )); \
	done < <(cat /tmp/ports); rm --force /tmp/ports; \
	source "${CONFIG_DIR}/${NAME}"; \
	newRule="L *:$$nextPort:${PRINTER}:9100 # ${DESC}"; \
	ForwardPort+=( "$$newRule" ); \
	printf "%s\n%s\n%s\n"	"# - - - - - - - - - - - - - - - - - - - - - - - - - - " \
								"# See /etc/mast/template for more informations" \
								"# - - - - - - - - - - - - - - - - - - - - - - - - - - " \
		> "${CONFIG_DIR}/.${NAME}"; \
	declare -p Compression RemoteHost RemoteUser RemotePort ServerAliveInterval ServerAliveCountMax StrictHostKeyChecking LocalUser IdentityFile ForwardPort BandwidthLimitation UploadLimit DownloadLimit >> "${CONFIG_DIR}/.${NAME}" \
		&& mv "${CONFIG_DIR}"/{.,}"${NAME}" \
		&& printf "\t%-50s\t%s\n" $$'$(call VALUE,'"$$newRule"$$')' $$'$(call SUCCESS,added)' \
		||    printf "\t%-50s\t%s\n" $$'$(call VALUE,'"$$newRule"$$')' $$'$(call ERROR,failed)'
	@chown -R ${APP}:${WEB_SERVER} "${CONFIG_DIR}"
	@chmod -R u=rwx,g=rwx,o= "${CONFIG_DIR}"
	rm --recursive --force /tmp/mast.busy


# Remove channel using its index
# @require: 	{string} 	NAME 		configuration name
# @require 	{integer}	ID 		channel index as given by 'list-channels'
remove-channel:
	@printf "Removing channel…\n"
	@if [[ ${ID} == -1 || -z ${ID} ]]; then \
		printf "\t%s.\n" $$'$(call ERROR,missing ID)' 1>&2; \
		exit 0; \
	else \
		source "${CONFIG_DIR}/${NAME}"; \
		removedRule="$${ForwardPort[${ID}]}"; \
		if [[ -z $$removedRule ]]; then \
			printf "\t%-50s\t%s\t%s\n" "rule "$$'$(call VALUE,#${ID})' $$'$(call WARNING,skipped)' $$'$(call INFO,(doesn\'t exists))' ; \
		else \
			unset 'ForwardPort[${ID}]'; \
			declare -p Compression RemoteHost RemoteUser RemotePort ServerAliveInterval ServerAliveCountMax StrictHostKeyChecking LocalUser IdentityFile ForwardPort BandwidthLimitation UploadLimit DownloadLimit \
			>> "${CONFIG_DIR}/.${NAME}" \
			&& mv "${CONFIG_DIR}"/{.,}"${NAME}" \
			&& printf "\t%-50s\t%s\n" $$'$(call VALUE,'"$$removedRule"$$')' $$'$(call SUCCESS,removed)' \
			||    printf "\t%-50s\t%s\n" $$'$(call VALUE,'"$$removedRule"$$')' $$'$(call ERROR,failed)'; \
		fi;\
	fi

# Adding a new host configuration require to provide it's NAME and REMOTE_HOST
# @require: {string} NAME configuration name
# @require: {string} REMOTE_HOST  IP address or FQDN
# @optional: {boolean} INTERACTIVE  require user input (default: true)
add-host: deploy-key
	@printf "Adding host…\n"
	@if [[ "${NAME}" == "none" || -z "${NAME}" || "${REMOTE_HOST}" == "none" || -z "${REMOTE_HOST}" ]]; then \
		printf "\t%s or %s.\n" $$'$(call ERROR,missing REMOTE_HOST)' $$'$(call ERROR,NAME)' 1>&2; \
		exit 0; \
	elif [[ "${NAME}" != "none" ]]; then \
		if [[ -f "${CONFIG_DIR}/${NAME}" ]]; then \
			printf "\t%-50s%s\t%s\n" $$'$(call VALUE,${NAME})' $$'$(call ERROR,failed)' $$'$(call INFO, (already exists))' 1>&2; \
			exit 0; \
		fi; \
		safe_name="$$(echo "${NAME}" | iconv -t ASCII//TRANSLIT | sed -e 's/[^A-Za-z0-9._-]/-/g')"; \
		cp ${CONFIG_DIR}/{template,"$${safe_name}"}; \
		sed -i 's/{{HOST}}/${REMOTE_HOST}/g' "${CONFIG_DIR}/$${safe_name}" \
		&& printf "\t%-50s%s\t%s\n" $$'$(call INFO,${NAME})' $$'$(call VALUE, ${REMOTE_HOST})' $$'$(call SUCCESS,added)'; \
		while ${INTERACTIVE} && true; do \
			read -p "$(shell printf "\tEditing…\t%s? [y/N]\n" $$'$(call VALUE,${CONFIG_DIR}/$${safe_name})' )" yn; \
			case $$yn in \
				[Yy]* ) \
					editor "${CONFIG_DIR}/$${safe_name}"; \
					printf "\nYou must %s the tunnel with:\n\t%s %s\n" $$'$(call WARNING,start –manually–)' $$'$(call INFO,sudo /etc/init.d/mast start $${safe_name})' 1>&2; \
					break;; \
				'') ;& \
				[Nn]*) \
					printf "\t%s\n" $$'$(call INFO,Skipping)'; \
					exit;; \
				* ) \
					printf "\t\tAnswer by %s or %s.\n" $$'$(call VALUE,yes)' $$'$(call VALUE,no)';; \
			esac; \
		done; \
	else \
		printf "Missing customer name…\t%s\n" "${NAME}"; \
	fi
	@chown -R ${APP}:${WEB_SERVER} "${CONFIG_DIR}"
	@chmod -R u=rwx,g=rwx,o= "${CONFIG_DIR}"


# Remove host using its configuration name
# @require: 	{string} 	NAME 		configuration name
remove-host:
	@printf "Removing host…\n\t%s\t\t" $$'$(call VALUE, ${NAME})'
	@if [[ "${NAME}" == "none" || -z "${NAME}" ]]; then \
		printf "%s host\'s NAME.\n" $$'$(call WARNING,invalid)' 1>&2; \
	elif [[ ! -e "${CONFIG_DIR}/${NAME}" ]]; then \
		printf "does %s.\n" $$'$(call WARNING,not exist)' 1>&2; \
	elif [[ ! -f "${CONFIG_DIR}/${NAME}" ]]; then \
		printf "%s host\'s file.\n" $$'$(call WARNING,invalid)' 1>&2; \
	else \
		source "${CONFIG_DIR}/${NAME}"; \
		ssh-keygen -q -R "$$RemoteHost" 2> /dev/null; \
		rm -f "${CONFIG_DIR}/${NAME}" && printf "%s\n" $$'$(call SUCCESS,done)' ||    printf "%s\n" $$'$(call ERROR,error)' 1>&2; \
	fi

# Install application network may not be setup, so don't deploy (ssh's key) on remote devices
install: check-system check-privileges create-ssh-key


config-ssh: deploy-key

# Copy infra public key on customer's node (defined by REMOTE_HOST)
# @optional: {string} 	REMOTE_USER		user on remote
# @require: {string} 	REMOTE_HOST 		server hostname or IP
# @warning: do NOT read ~/.ssh/config
deploy-key:
	@printf "Deploying…\t%s\n" $$'$(call VALUE, Public key)'
	@if [[ "${REMOTE_USER}" == "none" || -z "${REMOTE_USER}" || "${REMOTE_HOST}" == "none" || -z "${REMOTE_HOST}" ]]; then \
		printf "\t%s or %s.\n" $$'$(call ERROR,missing REMOTE_HOST)' $$'$(call ERROR,REMOTE_USER)' 1>&2; \
		exit 1; \
	else \
		printf "\t%s%-32s" $$'$(call INFO,copy public key to)' $$'$(call VALUE, ${REMOTE_USER}@${REMOTE_HOST})'; \
		sshpass -p "${REMOTE_INIT_PWD}" \
			ssh-copy-id -i "${SSH_KEYFILE}.pub" -o StrictHostKeyChecking=no -o ConnectTimeout=5 ${REMOTE_USER}@${REMOTE_HOST} &> /dev/null \
			&& printf "%s\n" $$'$(call SUCCESS,done)' \
			|| { printf "%s\n" $$'$(call ERROR,failed)'; exit 1; }; \
		printf "\n"; \
	fi


# Create keys pair on infra
#@alias: create-ssh-key
${SSH_KEYFILE}:
	@printf "Creating…\t%s\n" $$'$(call VALUE,SSH keys)'
		@[[ ! -d ${SSH_DIR} ]] && mkdir "${SSH_DIR}" || true
	@printf "\t%-50s%s" $$'$(call INFO,removing existing key)'
		@rm -f ${SSH_KEYFILE}{,.pub} \
			&& printf "%s\n" $$'$(call SUCCESS,done)' \
			||    printf "%s\n" $$'$(call ERROR,failed)'
	@chown -R ${APP} "${SSH_DIR}"

	@printf "\t%-50s%s" $$'$(call INFO,generating key)'
		@su - ${APP} -c 'ssh-keygen -q \
			-t rsa \
			-b 4096 \
			-f "${SSH_KEYFILE}" \
			-N "${EMPTY}" \
			-O permit-port-forwarding \
			-C "Automatically generated by MAST script"' \
			&& printf "%s\n" $$'$(call SUCCESS,done)' \
			||    printf "%s\n" $$'$(call ERROR,failed)'
	@chmod -R u=rwx,go= "${SSH_DIR}"

# Check files permission
check-privileges:
	@printf "Checking…\t%s\n" $$'$(call VALUE,Privileges)'

	@printf "\t%-50s\t" $$'$(call INFO,edit sudoers)'
	@if ! grep -iq 'mast' /etc/sudoers; then \
		echo "${APP} ALL= (ALL:ALL) NOPASSWD: /etc/init.d/mast,/usr/sbin/mast-utils" \
			>> /etc/sudoers \
		&& \
		echo "${WEB_SERVER} ALL= (ALL:ALL) NOPASSWD: /etc/init.d/mast,/usr/sbin/mast-utils" \
			>> /etc/sudoers \
		&& printf "$(call SUCCESS,done)\n" \
		||    printf "$(call ERROR,error)\n" 1>&2; \
	else \
		printf "%s (already existing)\n" $$'$(call WARNING,skipped)' 1>&2; \
	fi

	@# open privileges to ${WEB_SERVER} and ${APP} group.
	@# /!\ It is assumed ${REMOTE_USER} already exist on system
	@printf "\t%-50s\t" $$'$(call INFO,service\'s user)'
	@if ! getent passwd ${APP} > /dev/null; then \
		groupadd -r ${APP}; \
		useradd \
			--gid ${WEB_SERVER} \
			--groups ${APP} \
			--password "$$(mkpasswd "${REMOTE_INIT_PWD}")" \
			--create-home \
			--system ${APP} \
			--comment "MAST user" \
			&& printf "%s" $$'$(call SUCCESS,added)\n' \
			||    printf "%s" $$'$(call ERROR,failed)\n'; \
	else \
		printf "%s" $$'$(call WARNING,modified)\n'; \
		usermod --append --groups ${APP} ${REMOTE_USER}; \
	fi
	@usermod --append --groups ${WEB_SERVER} ${REMOTE_USER}
	@usermod --append --groups ${APP} ${WEB_SERVER}
	@newgrp - ${WEB_SERVER} &
	@# ensure that our user has a readable ~/.ssh directory
	@if [[ ! -d $$HOME/.ssh ]]; then \
		mkdir "$$HOME/.ssh" ; \
		chown -R $$SUDO_USER:$$SUDO_USER "$$HOME/.ssh" ; \
		chmod u=rwx,go= "$$HOME/.ssh" ; \
	fi

	@printf "\t%-50s\t" $$'$(call INFO,update permissions)'
	@[[ ! -d ${LOG_DIR} ]] && mkdir "${LOG_DIR}" || true
	@chown -R ${APP}:${WEB_SERVER} "${LOG_DIR}"
	@chmod -R u=rwx,g=rwx,o= "${LOG_DIR}"

	@[[ ! -d ${CONFIG_DIR} ]] && mkdir "${CONFIG_DIR}" || true
	@chown -R ${APP}:${WEB_SERVER} "${CONFIG_DIR}"
	@chmod -R u=rwx,g=rwx,o= "${CONFIG_DIR}"


# Check system status for dependencies
check-system:
	@printf "Checking…\t%s\n" $$'$(call VALUE,System)'
	@executables=( ${DEPS_CORE_INFRA} ${DEPS_CORE_CUSTOMER} ${DEPS_UTILS} ); \
	if ! type dpkg-query &> /dev/null; then \
		printf "You *MUST* install 'dpkg'\n"; \
		printf "\t→ %s %s\n" $$'$(call VALUE, apt-get install dpkg)'; \
		exit; \
	fi; \
	for e in $${executables[@]}; do \
		printf "\t%-50s" $$'$(call VALUE, '$$e$$')'; \
		if ! dpkg-query -s "$$e" &> /dev/null; then \
			printf "%12s\t" $$'$(call ERROR,missing)'; \
			printf "→ %s %s\n" $$'$(call INFO,apt-get install '$$e $$')'; \
		else \
			printf "%-12s\n" $$'$(call SUCCESS,installed)'; \
		fi \
	done

# Display basic help. For further information refer to the docs http://github.com/edouard-lopez/mast/README.md
usage:
	@printf "Usage…\n"
	@printf "\t%s: both commands require %s privilieges.\n" $$'$(call WARNING,warning)' $$'$(call VALUE,sudo)' 1>&2
	@printf "\n"
	@printf "\t%-50s%s %s\n" $$'$(call INFO,for full installation)' $$'$(call WARNING,sudo)' $$'$(call VALUE,make install)'


# Reset
_RESET_=\e[0m
# valid/green
_SUCCESS_=\e[0;32m
# blue/information
_INFO_=\e[0;36m
# blue/information
_DEBUG_=\e[0;37m
# red/error
_ERROR_=\e[1;31m
# yellow/warning
_WARNING_=\e[0;33m
# value/purple
_VALUE_=\e[0;35m

# Colours function helpers
SUCCESS=$(_SUCCESS_)$(1)$(_RESET_)
INFO=$(_INFO_)$(1)$(_RESET_)
DEBUG=$(_DEBUG_)$(1)$(_RESET_)
ERROR=$(_ERROR_)$(1)$(_RESET_)
WARNING=$(_WARNING_)$(1)$(_RESET_)
VALUE=$(_VALUE_)$(1)$(_RESET_)


