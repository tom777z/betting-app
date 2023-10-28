# betting-app

Django footbal betting application

Deployment:
1) Install following packages:
   pip install django
   pip install signals
   pip install django-bootstrap-v5
   pip install Pillow
   pip install psycopg2
   pip install django_extensions

2) Run db migration:
   python manage.py migrate

3) Create superuser:
   python manage.py createsuperuser

4) python manage.py runserver
   
5) Inside django admin, create following objects:
   Player
   Countries, Leagues, Teams, Round
