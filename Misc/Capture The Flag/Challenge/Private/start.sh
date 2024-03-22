#!/bin/sh
docker build -t ctf .
docker run -d -p 1740:1740 --net=host ctf
