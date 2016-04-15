FROM ubuntu:12.04

ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get install --yes \
            openssh-server

RUN mkdir /var/run/sshd

EXPOSE 22
CMD    ["/usr/sbin/sshd", "-D"]