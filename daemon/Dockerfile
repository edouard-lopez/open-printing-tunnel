FROM python:3.5.2

ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive
ARG DAEMON_USER=mast
ARG REMOTE_USER=coaxis
ARG REMOTE_INIT_PWD=C1i3ntRmSid3

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
            nginx \
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
        --comment "MAST user"
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
COPY mast /etc/init.d/
RUN chown ${DAEMON_USER}:www-data /etc/init.d/mast \
    && update-rc.d mast defaults > /dev/null

# Install mast-utils
COPY makefile /usr/sbin/mast-utils
RUN chown ${DAEMON_USER}:www-data /usr/sbin/mast-utils

# Create config directory and add template
COPY template /etc/mast/
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

COPY makefile /opt/mast/
COPY mast /opt/mast/

# Proxy
#RUN rm /etc/nginx/nginx.conf
#RUN rm /etc/nginx/mime.types
#COPY proxy-web/nginx.conf /etc/nginx/nginx.conf
#COPY proxy-web/mime.types /etc/nginx/mime.types
#COPY proxy-web/default.conf /etc/nginx/conf.d/default.conf
#COPY proxy-web/api.conf /etc/nginx/conf.d/api.conf

# Flask
RUN apt-get update && apt-get install -y \
    python3-venv \
    supervisor
WORKDIR /api
COPY ./api/ /api
COPY requirements.txt ./
RUN python3 -m pip install -r requirements.txt

RUN cd /opt/mast/ && make install

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

EXPOSE 5000