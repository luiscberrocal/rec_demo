#!/bin/sh
docker stop $(docker ps -qa)
docker-compose -f local.yml run django python manage.py admin_generator $1 > output/_admin_$1.py
echo " Saved ouput/_admin_$1.py"
