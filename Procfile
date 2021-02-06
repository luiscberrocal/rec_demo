release: python manage.py migrate

web: gunicorn config.wsgi:application
worker: celery worker -a config.celery_app --loglevel=info
beat: celery beat -a config.celery_app --loglevel=info
