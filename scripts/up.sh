#!/bin/sh
docker stop $(docker ps -qa)
docker-compose -f local_min.yml up

