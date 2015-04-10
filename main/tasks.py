from celery.task import periodic_task
from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from main.dropbox_api import Dropbox
from main.models import Audio


@periodic_task(ignore_result=True, run_every=timedelta(minutes=10))
def update_track_url():
    print 'UPDATE URLS:'
    hour_ago = timezone.now() - timedelta(hours=1)
    audio = Audio.objects.filter(Q(last_updated__gte=hour_ago) | Q(last_updated=None))
    print len(audio)
    db = Dropbox()
    for track in audio:
        track.url = db.get_abs_url(track.path)
        track.save()
