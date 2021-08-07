from celery import Celery
from decouple import config


REDIS_SERVER = config('REDIS_SERVER', 'redis')
app = Celery('tasks', broker=f'redis://{REDIS_SERVER}')


@app.task
def postprocess(job_list):
    pass