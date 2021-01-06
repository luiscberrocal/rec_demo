#!/bin/sh
docker stop $(docker ps -qa)
FILE=_serializers_$1.py
docker-compose -f local.yml run django python manage.py generate_serializers $1 -f $FILE
echo " Saved $FILE"
