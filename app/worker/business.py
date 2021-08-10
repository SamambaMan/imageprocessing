import cv2
import operator
from functools import reduce
from .blurrers import BLURRERS


def resize(input_image, params):
    size = [int(x) for x in params.split('x')]
    return [
        cv2.resize(image, size, interpolation=cv2.INTER_AREA)
        for image in input_image
    ]


def split(input_image, params):
    del params

    def splitsingle(image):
        height, width = image.shape[:2]
        hwidth, hheight = int(width/2), int(height/2)

        return [
            image[0:hheight, 0:hwidth],
            image[0:hheight, hwidth:width],
            image[hheight:height, 0:hwidth],
            image[hheight:height, hwidth:width],
        ]

    return reduce(
        operator.add,
        [
            splitsingle(image)
            for image in input_image
        ]
    )


def blur(input_image, params):
    return [
        BLURRERS[params](image)
        for image in input_image
    ]
