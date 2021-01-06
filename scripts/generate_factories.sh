#!/bin/sh
docker stop $(docker ps -qa)
FILE=factories_$1.py
docker-compose -f local_min.yml run django python manage.py generate_factories $1 --filename=$FILE
echo " Saved $FILE"
