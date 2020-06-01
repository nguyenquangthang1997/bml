from celery import Celery

app = Celery('proj', broker='redis://:@redis-bml:6379/15', include=['worker.tasks'])

BASEDIR = "./"
app.conf.broker_transport_options = {
    "max_retries": 3,
    "interval_start": 0,
    "interval_step": 0.2,
    "interval_max": 0.2,
}
