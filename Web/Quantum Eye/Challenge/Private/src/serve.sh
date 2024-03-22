#!/bin/sh
python3 -m hypercorn -b 0.0.0.0:80 --reload --workers 1 app:app
