import mock
import cv2
from collections import OrderedDict
from worker.pipeliner import (
    output_images,
    extract_filename,
    iterate_jobs,
    process_item
)

@mock.patch('worker.pipeliner.cv2.imwrite')
def test_output_image(_imw):
    # testing if the image filename buildup is correct
    imagelist = ['fakeone', 'faketwo', 'fakethree']
    striped_filename = 'somefilename'
    extension = 'jpg'

    output_images(imagelist, striped_filename, extension)

    _imw.assert_any_call(
        f'/var/file_deposit/{striped_filename}-0.{extension}',
        'fakeone'
    )
    _imw.assert_any_call(
        f'/var/file_deposit/{striped_filename}-1.{extension}',
        'faketwo'
    )
    _imw.assert_any_call(
        f'/var/file_deposit/{striped_filename}-2.{extension}',
        'fakethree'
    )
    assert _imw.call_count == 3


def test_extradt_filename():
    job_item = {
        'filename': 'a_file_name.jpg.png.jpeg',
        'output': 'png'
    }
    filename, striped_filename, output = extract_filename(job_item)

    assert filename == 'a_file_name.jpg.png.jpeg'
    assert striped_filename == 'a_file_name.jpg.png'
    assert output == 'png'


@mock.patch('worker.business.resize')
@mock.patch('worker.business.split')
@mock.patch('worker.business.blur')
def test_iterate_job(_resi, _spli, _blur):
    job_list = OrderedDict([
        ('resize', '200x200'),
        ('split', True),
        ('blur', 'median'),
    ])
    image_list = [1, 2, 3, 4]

    iterate_jobs(image_list, job_list)


@mock.patch(
    'worker.pipeliner.cv2.imread', 
    return_value=cv2.imread('tests/fixtures/tv-pattern.png')
)
@mock.patch('worker.pipeliner.cv2.imwrite')
def test_process_item(_imwr, _imre):
    job_item = OrderedDict([
        ('filename', 'output.jpg'),
        ('output', 'png'),
        ('resize', '200x200'),
        ('split', True),
        ('blur', 'median'),
    ])

    process_item(job_item)
    
    _imre.assert_called_once_with(f'/var/file_deposit/output.jpg')
    assert _imwr.call_count == 4