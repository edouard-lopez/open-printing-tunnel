FROM python:3.5.2

ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive
ARG DAEMON_USER=mast
ARG REMOTE_USER=coaxis
ARG REMOTE_INIT_PWD=C1i3ntRmSid3

RUN apt-get update \
    && apt-get install --yes --force-yes --no-install-recommends --no-install-suggests \
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
            trickle \
            vim-tiny \
            wget \
            whois
#	&& rm -rf /var/lib/apt/lists/*

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
RUN apt-get update && apt-get install --yes --force-yes --no-install-recommends --no-install-suggests \
            ca-certificates \
            nginx \
            supervisor

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log

RUN rm /etc/nginx/nginx.conf
RUN rm /etc/nginx/mime.types
COPY proxy-web/nginx.conf /etc/nginx/nginx.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY proxy-web/mime.types /etc/nginx/mime.types
COPY proxy-web/conf.d /etc/nginx/conf.d/
EXPOSE 80 443

# Flask
RUN apt-get update && apt-get install --yes --force-yes --no-install-recommends --no-install-suggests \
    gunicorn \
    python3-venv \
    supervisor
WORKDIR /daemon
COPY ./ /daemon
COPY requirements.txt ./
RUN python3 -m pip install -r requirements.txt

RUN cd /opt/mast/ && make install

COPY config/ /etc/supervisor/conf.d
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/prod.conf"]

EXPOSE 5000