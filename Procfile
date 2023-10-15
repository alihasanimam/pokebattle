release: python manage.py migrate

web: gunicorn pokebattle.wsgi --log-file -

worker: python manage.py rqworker default