FROM ubuntu:12.04


ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive


RUN apt-get update \
    && apt-get install --yes \
            bmon \
            dpkg \
            git \
            htop \
            iftop \
            make \
            wget

RUN apt-get update \
    && apt-get install --yes \
            autossh \
            libc-bin \
            openssh-client \
            sshpass \
            sudo \
            trickle \
            whois


COPY makefile /opt/opt/
COPY mast /opt/opt/
COPY template /opt/opt/
COPY webapp /opt/webapp/

RUN adduser \
    --quiet \
    --disabled-password \
    --shell /bin/bash \
    --home /home/coaxis \
    --gecos "Open Print Tunnel" \
    coaxis \
    && echo "coaxis:C1i3ntRmSid3" | chpasswd \
    && addgroup coaxis sudo

VOLUME ['/etc/mast']

COPY entrypoint.sh /
RUN chmod 755 /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]