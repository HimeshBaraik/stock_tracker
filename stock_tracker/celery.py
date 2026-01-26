from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab # This is used to schedule the tasks


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_tracker.settings')

app = Celery('stock_tracker')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'fetch-stock-data-every-ten-seconds': {
        'task': 'mainapp.tasks.fetch_stocks_data_task',
        'schedule': 10.0,
        'args': (['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS'],),
    },
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request}")