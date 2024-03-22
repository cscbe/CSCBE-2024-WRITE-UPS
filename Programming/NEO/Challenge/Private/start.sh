#!/bin/sh
docker build -t neo .
docker run -d -p 1338:1338 neo

