import os
from celery.schedules import crontab


CELERY_BROKER_URL = f'amqp://'+os.environ.get('RABBITMQ_HOST')

CELERY_BEAT_SCHEDULE = {
    'parse': {
        'task': 'testsuite.tasks.cleanup_outdated_testruns',
        'schedule': crontab(minute='*/1'),
    },
}