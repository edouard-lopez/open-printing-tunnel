FROM php:5.5-apache


ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive
ENV OPT_USER coaxis
ENV OPT_PASSWORD C1i3ntRmSid3
ENV WEBAPP_DIR /var/www/html/webapp

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

# Mast
COPY daemon/makefile /opt/mast/
COPY daemon/mast /opt/mast/
COPY daemon/template /opt/mast/
COPY webapp /opt/webapp/

RUN adduser \
    --quiet \
    --disabled-password \
    --shell /bin/bash \
    --home /home/${OPT_USER} \
    --gecos "Open Print Tunnel" \
    ${OPT_USER} \
    && echo "${OPT_USER}:${OPT_PASSWORD}" | chpasswd \
    && addgroup ${OPT_USER} sudo

# Webapp
RUN rm -rf /var/www/html
COPY webapp/application ${WEBAPP_DIR}/application
COPY webapp/resources ${WEBAPP_DIR}/resources
COPY webapp/system ${WEBAPP_DIR}/system
COPY webapp/index.php ${WEBAPP_DIR}

COPY webapp/resources/server/webapp.apache.conf /etc/apache2/sites-enabled/opt-webapp.conf
COPY webapp/resources/server/php.ini /usr/local/etc/php/
RUN chown -R www-data:www-data /var/www/html
RUN a2enmod rewrite

RUN cd /opt/mast/ && make install

EXPOSE 80