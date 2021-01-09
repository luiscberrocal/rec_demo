#!/bin/sh
docker stop $(docker ps -qa)
FILE=output/_serializers_tests_$2.py
docker-compose -f local_min.yml run django python manage.py generate_serializers_tests rec_demo.$1.api.serializers.$2 -f $FILE
echo " Saved $FILE"
