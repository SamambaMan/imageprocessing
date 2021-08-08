import cv2
import mock
import operator
from functools import reduce
from worker.business import (
    resize,
    split,
    blur,
)


def test_resize_lower():
    images = [cv2.imread('tests/fixtures/tv-pattern.png')]

    resulting = resize(images, '200x300')

    height, width = resulting[0].shape[:2]

    assert width == 200
    assert height == 300


def test_resize_higher():
    images = [cv2.imread('tests/fixtures/tv-pattern.png')]

    resulting = resize(images, '1200x4000')

    height, width = resulting[0].shape[:2]

    assert width == 1200
    assert height == 4000


def test_resize_many():
    # this method is not intented to be used like this, but 
    # is a nice way to be sure it will resize all the same
    images = [
        cv2.imread('tests/fixtures/test-pattern.jpeg'),
        cv2.imread('tests/fixtures/tv-pattern.png')
    ]

    resulting = resize(images, '1200x4000')

    height1, width1 = resulting.pop().shape[:2]
    height2, width2 = resulting.pop().shape[:2]

    assert width1 == width2 == 1200
    assert height1 == height2 == 4000


def test_split():
    images = [
        cv2.imread('tests/fixtures/tv-pattern.png'),
        cv2.imread('tests/fixtures/test-pattern.jpeg'),
    ]

    result = split(images, 'yay')

    shapes = [item.shape[:2] for item in result]
    shapes = reduce(
        operator.add,
        shapes
    )

    reference = (
        # image 1
        300, 480, 300, 480, 300, 480, 300, 480,
        # image 2
        94, 133, 94, 134, 95, 133, 95, 134
    )

    assert all(
        [a == b for a, b in zip(shapes, reference)]
    )


@mock.patch('worker.blurrers.cv2.GaussianBlur')
def test_blur(_gauss):
    # won`t test python here. just checking
    # if the job is done

    blur(['yay'], 'gaussian')

    _gauss.assert_called_once_with('yay', (5, 5), 0)
