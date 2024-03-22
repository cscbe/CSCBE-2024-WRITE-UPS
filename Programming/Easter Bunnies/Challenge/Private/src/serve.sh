#!/bin/sh
socat \
    -T60 \
    TCP-LISTEN:1338,reuseaddr,fork \
    EXEC:"timeout 600 ./bunnies.py"