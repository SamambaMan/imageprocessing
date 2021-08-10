import cv2
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


def extract_filename(job_list, image_filename):
    stripped_filename = '.'.join(image_filename.split('.')[:-1])
    return stripped_filename, job_list['output']


def iterate_jobs(image_list, job_item):
    METHODS = {
        'resize': resize,
        'split': split,
        'blur': blur,
    }

    operations = job_item['operations']

    for operation, params in operations:
        image_list = METHODS[operation](
            image_list,
            params
        )
    return image_list


def process_item(job_list, image_filename):
    """
        Process a image with the job_list parameters

        :param job_list: the job list that applies to every image
            in the bulk.
        :param image: image filename to work on
    """
    # prepare de parametrized job caracteristics
    stripped_filename, output = extract_filename(
        job_list,
        image_filename
    )

    image_list = [cv2.imread(f'/var/file_deposit/{image_filename}')]

    # iterate ordered keys and do what must be done acording to
    # user`s demands
    image_list = iterate_jobs(image_list, job_list)

    output_images(
        image_list,
        stripped_filename,
        output
    )
