from celery import Celery
from collections import OrderedDict
from decouple import config
from .business import (
    resize,
    split,
    blur
)


REDIS_SERVER = config('REDIS_SERVER', 'redis')
app = Celery('tasks', broker=f'redis://{REDIS_SERVER}')

ORDERED_METHOD_DICT = OrderedDict([
    ('resize', resize),
    ('split', split),
    ('blur', blur),
])


@app.task
def postprocess(job_list):
    pass
