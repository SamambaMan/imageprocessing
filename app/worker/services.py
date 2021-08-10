from celery import Celery
from decouple import config
from .pipeliner import process_item


REDIS_SERVER = config('REDIS_SERVER', 'redis')
app = Celery('tasks', broker=f'redis://{REDIS_SERVER}')


@app.task
def postprocess(job_list, image_filename_list):
    """
        Async method to process a job_list into an image list.

        :param job_list: the job list that applies to every image
            in the bulk.
        :param image_filename_list: list of images filenames to work on
    """
    for image_filename in image_filename_list:
        process_item_async.delay(job_list, image_filename)


@app.task
def process_item_async(job_list, image_filename):
    """
        This wrapper allows to execute item processing in parallel.
        For parallelism control and server load, this method assumes
        that the concurrency level of the server is the number of cpus
        available, since this is the Celery default
    """
    process_item(job_list, image_filename)
