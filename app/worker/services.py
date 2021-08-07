import cv2
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


def process_item(job_item):
    # prepare de parametrized job caracteristics
    filename = job_item.pop('filename')
    output = job_item.pop('output')

    imagelist = [cv2.imread(f'/var/file_deposit/{filename}')]

    # iterate ordered keys and do what must be done acording to 
    # user`s demands
    for key in job_item.keys():
        ORDERED_METHOD_DICT[key](
            imagelist,
            job_item[key]
        )


@app.task
def postprocess(job_list):
    # this process assumes that the user will 
    # specify the order of the operations.
    for job in job_list:
        process_item(job)
