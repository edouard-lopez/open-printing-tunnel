FROM python:3.5-slim-stretch

# -------------------------------------------
# Daemon APT Install
# -------------------------------------------
ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive
ARG DAEMON_USER=mast
ARG REMOTE_USER=coaxis
ARG REMOTE_INIT_PWD=C1i3ntRmSid3

RUN sed --in-place 's!$! non-free!' /etc/apt/sources.list  # add non-free repositories from snmp-mibs-downloader

ENV BUILD_DEPENDENCIES apt-utils \
  libc-dev \
  gcc \
  gnupg2
RUN apt-get update \
  && apt-get install --yes --no-install-recommends \
  $BUILD_DEPENDENCIES \
  curl \
  && curl -sL https://deb.nodesource.com/setup_10.x | bash - \
  && rm --recursive --force /var/lib/apt/lists/*
RUN apt-get update \
  && apt-get install --yes --no-install-recommends --no-install-suggests \
  autossh \
  dpkg \
  gawk \
  fping \
  grep \
  htop \
  libsmi2-dev \
  libffi-dev \
  libc-bin \
  make \
  nano \
  nmap \
  nodejs \
  openssh-server \
  openssh-client \
  snmp \
  snmpd \
  snmp-mibs-downloader \
  sshpass \
  sudo \
  trickle \
  wget \
  whois \
  ca-certificates \
  nginx \
  supervisor \
  && rm -rf /var/lib/apt/lists/*

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

WORKDIR /opt/mast
COPY makefile ./
RUN make install


# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
  && ln -sf /dev/stderr /var/log/nginx/error.log
RUN rm /etc/nginx/nginx.conf
RUN rm /etc/nginx/mime.types
COPY proxy-web/nginx.conf /etc/nginx/nginx.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY proxy-web/mime.types /etc/nginx/mime.types
COPY proxy-web/conf.d /etc/nginx/conf.d/
EXPOSE 80


WORKDIR /api
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./api /api
EXPOSE 5000


WORKDIR /frontend
COPY ./frontend/package.json /frontend/
RUN npm install --production
COPY ./frontend /frontend
EXPOSE 8080

VOLUME ["/etc/mast", "/home/mast/.ssh"]

# install BATS for testing
RUN npm install -g bats
COPY ./test /test

COPY config/ /etc/supervisor/conf.d
COPY help-me.mk /
RUN apt-get purge --yes --auto-remove $BUILD_DEPENDENCIES
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/prod.conf"]
