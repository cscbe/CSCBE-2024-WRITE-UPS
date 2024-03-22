#!/bin/sh
sudo nginx
gunicorn 'app:app' \
    --bind '0.0.0.0:1337' \
    --workers 1 \
    --access-logfile "-" \
    --error-logfile "-"
