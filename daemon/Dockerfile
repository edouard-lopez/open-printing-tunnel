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
EXPOSE 80


# FLASK API
RUN apt-get update && apt-get install --yes --force-yes --no-install-recommends --no-install-suggests \
    gunicorn \
    python3-venv \
    supervisor
WORKDIR /daemon
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./ /daemon
EXPOSE 5000


# FRONTEND
# gpg keys listed at https://github.com/nodejs/node
RUN set -ex \
  && for key in \
    9554F04D7259F04124DE6B476D5A82AC7E37093B \
    94AE36675C464D64BAFA68DD7434390BDBE9B9C5 \
    0034A06D9D9B0064CE8ADF6BF1747F4AD2306D93 \
    FD3A5288F042B6850C66B31F09FE44734EB7990E \
    71DCFD284A79C3B38668286BC97EC7A07EDE3FC1 \
    DD8F2338BAE7501E3DD5AC78C273792F7D83545D \
    B9AE9905FFD7803F25714661B63B535A4C206CA9 \
    C4F0DFFF4E8C1A8236409D08E73BC641CC11F4C8 \
  ; do \
    gpg --keyserver ha.pool.sks-keyservers.net --recv-keys "$key"; \
  done

ENV NPM_CONFIG_LOGLEVEL info
ENV NODE_VERSION 4.4.7

RUN buildDeps='xz-utils' \
    && set -x \
    && apt-get update && apt-get install -y $buildDeps --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-x64.tar.xz" \
    && curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt.asc" \
    && gpg --batch --decrypt --output SHASUMS256.txt SHASUMS256.txt.asc \
    && grep " node-v$NODE_VERSION-linux-x64.tar.xz\$" SHASUMS256.txt | sha256sum -c - \
    && tar -xJf "node-v$NODE_VERSION-linux-x64.tar.xz" -C /usr/local --strip-components=1 \
    && rm "node-v$NODE_VERSION-linux-x64.tar.xz" SHASUMS256.txt.asc SHASUMS256.txt \
    && apt-get purge -y --auto-remove $buildDeps

RUN mkdir -p /frontend
WORKDIR /frontend

COPY /frontend/package.json /frontend/
RUN npm install --production
COPY ./frontend/ /frontend
EXPOSE 8080


RUN cd /opt/mast/ && make install
COPY config/ /etc/supervisor/conf.d
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/prod.conf"]
