#!/usr/bin/env bash

set -x

# Start the first process
cd app || exit
waitress-serve --port=80 --call app:create_app &
# gunicorn -w 4 'app:create_app()' &

# Start the second process
cd ../admin-simulation || exit
python main.py &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?