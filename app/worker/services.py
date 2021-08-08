from celery import Celery
from decouple import config
from .pipeliner import process_item


REDIS_SERVER = config('REDIS_SERVER', 'redis')
app = Celery('tasks', broker=f'redis://{REDIS_SERVER}')


@app.task
def postprocess(job_list):
    # this process assumes that the user will
    # specify the order of the operations.
    for job in job_list:
        process_item(job)
