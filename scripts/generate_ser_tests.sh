#!/bin/sh
docker stop $(docker ps -qa)
FILE=output/_serializers_tests_$2.py
docker-compose -f local.yml run django python manage.py generate_serializers_tests alpha_clinic.$1.api.serializers.$2 -f $FILE
echo " Saved $FILE"
