import mock
import cv2
from collections import OrderedDict
from worker.pipeliner import (
    output_images,
    extract_filename,
    iterate_jobs,
    process_item
)


def Any():
    # quickand dirty compare to anything, no need to test
    # image processing here
    class Any():
        def __eq__(self, other):
            return True
    return Any()


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


def test_extract_filename():
    job_item = {
        'output': 'png'
    }

    stripped_filename, output = extract_filename(
        job_item,
        'a_file_name.jpg.png.jpeg'
    )

    assert stripped_filename == 'a_file_name.jpg.png'
    assert output == 'png'


@mock.patch('worker.pipeliner.resize', return_value=[2])
@mock.patch('worker.pipeliner.split', return_value=[3])
@mock.patch('worker.pipeliner.blur', return_value=[4])
def test_iterate_job(_blur, _spli, _resi):
    job_list = {
        'operations': [
            ('resize', '200x200'),
            ('split', True),
            ('blur', 'median'),
        ]
    }
    image_list = [1]

    result = iterate_jobs(image_list, job_list)
    
    _resi.assert_called_once_with([1], '200x200')
    _spli.assert_called_once_with([2], True)
    _blur.assert_called_once_with([3], 'median')

    assert result[0] == 4


@mock.patch(
    'worker.pipeliner.cv2.imread', 
    return_value=cv2.imread('tests/fixtures/tv-pattern.png')
)
@mock.patch('worker.pipeliner.cv2.imwrite')
def test_process_item(_imwr, _imre):
    job_item = {
        'output': 'png',
        'operations': [
            ('resize', '200x200'),
            ('split', True),
            ('blur', 'median'),
        ]
    }

    process_item(job_item, 'output.jpg')

    _imre.assert_called_once_with(f'/var/file_deposit/output.jpg')

    _imwr.assert_any_call('/var/file_deposit/output-0.png', Any())
    _imwr.assert_any_call('/var/file_deposit/output-1.png', Any())
    _imwr.assert_any_call('/var/file_deposit/output-2.png', Any())
    _imwr.assert_any_call('/var/file_deposit/output-3.png', Any())
