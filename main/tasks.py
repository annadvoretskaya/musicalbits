from celery.task import periodic_task
from datetime import timedelta


@periodic_task(ignore_result=True, run_every=timedelta(seconds=5))
def test_task():
    print 'HALLO'
