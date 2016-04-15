FROM ubuntu:12.04

ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get install --yes \
            openssh-server

RUN mkdir /var/run/sshd

RUN adduser \
    --quiet \
    --disabled-password \
    --shell /bin/bash \
    --home /home/coaxis \
    --gecos "Open Print Tunnel" \
    coaxis \
    && echo "coaxis:C1i3ntRmSid3" | chpasswd \
    && addgroup coaxis sudo

EXPOSE 22
CMD    ["/usr/sbin/sshd", "-D"]