#!/bin/sh

cd /opt/opt \
    && make install

exec "$@"