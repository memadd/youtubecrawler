from __future__ import absolute_import
import time
from subprocess import call
from celery import Celery
from celery.schedules import crontab

app = Celery('test_celery',broker='amqp://admin:mypass@rabbit:5672',backend='rpc://',include=['tasks'])

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    with open("playlists") as f:
        playlists = f.readlines()
    playlists = [x.strip() for x in playlists]
    for playlist in playlists:
        # sender.add_periodic_task(
        #     crontab(hour=7, minute=30),
        #     crawl_playlist.s(playlist),
        # )
        sender.add_periodic_task(3600.0, crawl_playlist.s(playlist), name='crawl every 10')



@app.task
def crawl_playlist(playlist):
    call(['docker', 'exec',  'youtubecrawly_scrapyd_1', 'sh', '/code/youtube/run_spider.sh', playlist])