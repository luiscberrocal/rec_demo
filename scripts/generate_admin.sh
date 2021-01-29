#!/bin/sh
docker stop $(docker ps -qa)
docker-compose -f local_min.yml run django python manage.py admin_generator $1 > output/_admin_$1.py
echo " Saved ouput/_admin_$1.py"
