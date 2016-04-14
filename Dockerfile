FROM php:5.5-apache


ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive


RUN apt-get update \
    && apt-get install --yes \
            aha \
            autossh \
            bmon \
            dpkg \
            git \
            htop \
            iftop \
            libc-bin \
            make \
            openssh-client \
            sshpass \
            sudo \
            sudo \
            trickle \
            wget \
            whois

# Mast
COPY daemon/makefile /opt/mast/
COPY daemon/mast /opt/mast/
COPY daemon/template /opt/mast/
COPY daemon/webapp /opt/webapp/

RUN adduser \
    --quiet \
    --disabled-password \
    --shell /bin/bash \
    --home /home/coaxis \
    --gecos "Open Print Tunnel" \
    coaxis \
    && echo "coaxis:C1i3ntRmSid3" | chpasswd \
    && addgroup coaxis sudo

# Webapp
RUN rm -rf /var/www/html
COPY webapp/application /var/www/html/application
COPY webapp/resources /var/www/html/resources
COPY webapp/system /var/www/html/system
COPY webapp/index.php /var/www/html

RUN chown -R www-data:www-data /var/www/html
RUN a2enmod rewrite


COPY entrypoint.sh /
RUN chmod 755 /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]