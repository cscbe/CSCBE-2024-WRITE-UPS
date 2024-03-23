#!/bin/sh
socat \
    -T15 \
    TCP-LISTEN:1338,reuseaddr,fork \
    EXEC:"timeout 15 ./server.py"