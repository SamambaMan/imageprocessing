import cv2
from worker.blurrers import (
    updownsampling,
    gaussian,
    
)


def test_blurrers_updownsampling():
    image = cv2.imread('tests/fixtures/tv-pattern.png')
    resulting = updownsampling(image)

