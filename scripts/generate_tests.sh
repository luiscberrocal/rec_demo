#!/bin/sh
docker stop $(docker ps -qa)
FILE=output/_tests_$1.py
docker-compose -f local_min.yml run django python manage.py generate_model_test_cases $1 > $FILE
echo " Saved $FILE"
