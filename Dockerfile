FROM ubuntu:12.04


ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive


RUN apt-get update \
    && apt-get install --yes wget make git

COPY makefile /opt/opt/
COPY mast /opt/opt/
COPY template /opt/opt/
COPY webapp /opt/

RUN adduser \
    --quiet \
    --disabled-password \
    --shell /bin/bash \
    --home /home/coaxis \
    --gecos "Open Print Tunnel" \
    coaxis \
    && echo "coaxis:C1i3ntRmSid3" | chpasswd \
    && addgroup coaxis sudo
RUN cd /opt/opt \
    && make install

VOLUME opt-templates:/etc/mast