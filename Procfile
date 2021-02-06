release: python manage.py migrate

web: gunicorn config.wsgi:application
worker: celery worker -A config.celery_app --loglevel=info
beat: celery beat -A config.celery_app --loglevel=info
