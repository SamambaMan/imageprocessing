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


def output_images(imagelist, striped_filename, extension):
    for i, image in enumerate(imagelist):
        cv2.imwrite(
            f'/var/file_deposit/{striped_filename}-{i}.{extension}',
            image
        )


def process_item(job_item):
    # prepare de parametrized job caracteristics
    filename = job_item.pop('filename')
    striped_filename = '.'.join(filename.split('.')[:-1])
    output = job_item.pop('output')

    imagelist = [cv2.imread(f'/var/file_deposit/{filename}')]

    # iterate ordered keys and do what must be done acording to
    # user`s demands
    for key in job_item.keys():
        imagelist = ORDERED_METHOD_DICT[key](
            imagelist,
            job_item[key]
        )

    output_images(
        imagelist,
        striped_filename,
        output
    )


@app.task
def postprocess(job_list):
    # this process assumes that the user will
    # specify the order of the operations.
    for job in job_list:
        process_item(job)
