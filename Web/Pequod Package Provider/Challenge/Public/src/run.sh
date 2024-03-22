sudo nginx &
gunicorn -w 1 --threads 8 'app:app' -b 127.0.0.1:4000 --log-level=verbose --access-logfile -