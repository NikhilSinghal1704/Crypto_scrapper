from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Setting the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')


app.config_from_object('django.conf:settings', namespace='CELERY')

# Loading task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))