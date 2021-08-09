import cv2
from collections import OrderedDict
from .business import (
    resize,
    split,
    blur
)


def output_images(imagelist, striped_filename, extension):
    for i, image in enumerate(imagelist):
        cv2.imwrite(
            f'/var/file_deposit/{striped_filename}-{i}.{extension}',
            image
        )


def extract_filename(job_item):
    filename = job_item.pop('filename')
    striped_filename = '.'.join(filename.split('.')[:-1])
    output = job_item.pop('output')
    return filename, striped_filename, output


def iterate_jobs(imagelist, job_item):
    ORDERED_METHOD_DICT = OrderedDict([
        ('resize', resize),
        ('split', split),
        ('blur', blur),
    ])

    for key in job_item.keys():
        imagelist = ORDERED_METHOD_DICT[key](
            imagelist,
            job_item[key]
        )
    return imagelist


def process_item(job_item):
    # prepare de parametrized job caracteristics
    filename, striped_filename, output = extract_filename(job_item)

    imagelist = [cv2.imread(f'/var/file_deposit/{filename}')]

    # iterate ordered keys and do what must be done acording to
    # user`s demands
    imagelist = iterate_jobs(imagelist, job_item)

    output_images(
        imagelist,
        striped_filename,
        output
    )
