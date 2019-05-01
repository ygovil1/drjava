release: python manage.py showmigrations; python manage.py makemigrations; python manage.py migrate; python manage.py showmigrations 
web: gunicorn backend.wsgi --log-file -