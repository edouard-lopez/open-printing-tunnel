FROM php:5.5-apache


ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive
ARG DAEMON_USER=mast
ARG REMOTE_USER=coaxis
ARG REMOTE_INIT_PWD=C1i3ntRmSid3
ARG WEBAPP_DIR=/var/www/html/webapp

RUN apt-get update \
    && apt-get install --yes \
            aha \
            autossh \
            bmon \
            dpkg \
            gawk \
            git \
            grep \
            htop \
            iftop \
            libc-bin \
            make \
            openssh-client \
            sshpass \
            sudo \
            supervisor \
            trickle \
            vim-tiny \
            wget \
            whois

# DAEMON
# Create users
RUN groupadd -r ${DAEMON_USER} \
    && useradd \
        --gid www-data \
        --groups ${DAEMON_USER} \
        --password "$$(mkpasswd "${REMOTE_INIT_PWD}")" \
        --create-home \
        --system ${DAEMON_USER} \
        --comment "MAST user" \
RUN adduser \
        --quiet \
        --disabled-password \
        --shell /bin/bash \
        --home /home/${REMOTE_USER} \
        --gecos "Open Print Tunnel" \
        ${REMOTE_USER} \
    && echo "${REMOTE_USER}:${REMOTE_INIT_PWD}" | chpasswd \
    && addgroup ${REMOTE_USER} sudo

# Install service
COPY daemon/mast /etc/init.d/
RUN chown ${DAEMON_USER}:www-data /etc/init.d/mast \
    && update-rc.d mast defaults > /dev/null

# Install mast-utils
COPY daemon/makefile /usr/sbin/mast-utils
RUN chown ${DAEMON_USER}:www-data /usr/sbin/mast-utils

# Create config directory and add template
COPY daemon/template /etc/mast/
RUN chmod u=rw,go= /etc/mast/template \
    && chown ${DAEMON_USER}:www-data /etc/mast/template

# Create directories for: log, pid and lock
RUN mkdir /var/log/mast \
          /var/run/mast \
          /var/lock/mast \
    && chown -R ${DAEMON_USER}:www-data \
            /etc/mast \
            /var/log/mast \
            /var/run/mast \
            /var/lock/mast \
    && chmod -R u=rwx,g=rwx,o= \
            /etc/mast \
            /var/log/mast \
            /var/run/mast \
            /var/lock/mast

COPY daemon/makefile /opt/mast/
COPY daemon/mast /opt/mast/
COPY webapp /opt/webapp/

# Webapp
RUN rm -rf /var/www/html
RUN mkdir ${WEBAPP_DIR}
VOLUME [ "${WEBAPP_DIR}" ]

COPY webapp/resources/server/webapp.apache.conf /etc/apache2/sites-enabled/opt-webapp.conf
COPY webapp/resources/server/php.ini /usr/local/etc/php/
RUN chown -R ${REMOTE_USER}:www-data "${WEBAPP_DIR}" \
    && a2enmod rewrite


RUN cd /opt/mast/ && make install

EXPOSE 80