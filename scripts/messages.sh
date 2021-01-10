#!/bin/sh
docker stop $(docker ps -qa)

if [ $1 == '-a' ] || [ $1 == '-m' ]
then
echo '>>>>>> MAKING'
docker-compose -f local_min.yml run django python manage.py makemessages --locale=es --extension=html,py
else
echo 'Make messages skipped'
pwd
fi

if [ $1 == '-a' ] || [ $1 == '-c' ]
then
echo '>>>>> COMPILING'
docker-compose -f local_min.yml run django python manage.py compilemessages
else
echo 'Compiling messages skipped'
pwd
fi


