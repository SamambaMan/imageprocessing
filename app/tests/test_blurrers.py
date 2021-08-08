import cv2
import mock
from worker.blurrers import (
    updownsampling,
    bilateral,
    median,
    gaussian,
)


@mock.patch('worker.blurrers.cv2.pyrUp')
@mock.patch('worker.blurrers.cv2.pyrDown')
def test_blurrers_updownsampling(_pdown, _pup):
    image = cv2.imread('tests/fixtures/tv-pattern.png')
    resulting = updownsampling(image)

    _pup.assert_called_once()
    _pdown.assert_called_once()


def test_blurrers_updownsampling_maintain():
    image = cv2.imread('tests/fixtures/tv-pattern.png')
    resulting = updownsampling(image)

    width, height = resulting.shape[:2]
    assert width == 600
    assert height == 960


@mock.patch('worker.blurrers.cv2.bilateralBlur')
def test_blurrers_bilateral(_gbur):
    image = cv2.imread('tests/fixtures/tv-pattern.png')
    resulting = bilateral(image)

    _gbur.assert_called_once_with(image, (5, 5), 0)


def test_blurrers_bilateral_maintain():
    image = cv2.imread('tests/fixtures/tv-pattern.png')
    resulting = bilateral(image)

    width, height = resulting.shape[:2]
    assert width == 600
    assert height == 960


@mock.patch('worker.blurrers.cv2.bilateralFilter')
def test_blurrers_bilateral(_gbil):
    image = cv2.imread('tests/fixtures/tv-pattern.png')
    resulting = bilateral(image)

    _gbil.assert_called_once_with(image, 9, 75, 75)


def test_blurrers_bilateral_maintain():
    image = cv2.imread('tests/fixtures/tv-pattern.png')
    resulting = bilateral(image)

    width, height = resulting.shape[:2]
    assert width == 600
    assert height == 960


@mock.patch('worker.blurrers.cv2.medianBlur')
def test_blurrers_median(_gmedi):
    image = cv2.imread('tests/fixtures/tv-pattern.png')
    resulting = median(image)

    _gmedi.assert_called_once_with(image, 5)


def test_blurrers_median_maintain():
    image = cv2.imread('tests/fixtures/tv-pattern.png')
    resulting = median(image)

    width, height = resulting.shape[:2]
    assert width == 600
    assert height == 960


@mock.patch('worker.blurrers.cv2.GaussianBlur')
def test_blurrers_gaussian(_gauss):
    image = cv2.imread('tests/fixtures/tv-pattern.png')
    resulting = gaussian(image)

    _gauss.assert_called_once_with(image, (5, 5), 0)


def test_blurrers_gaussian_maintain():
    image = cv2.imread('tests/fixtures/tv-pattern.png')
    resulting = gaussian(image)

    width, height = resulting.shape[:2]
    assert width == 600
    assert height == 960
