python manage.py runserver

celery -A stock_tracker.celery worker --pool=solo -l info 

celery -A stock_tracker beat -l info
