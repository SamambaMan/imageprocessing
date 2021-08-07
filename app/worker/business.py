import cv2
import operator
from functools import reduce
from .blurrers import BLURRERS


def resize(input, task):
    size = [int(x) for x in task.split('x')]
    return [
        cv2.resize(image, size, interpolation=cv2.INTER_AREA)
        for image in input
    ]


def split(input, task):
    def splitsingle(image):
        width, height = image.shape[:2]
        hwidth, hheight = int(width/2), int(height/2)

        return [
            image[0:hwidth, 0:hheight],
            image[hwidth:width, 0:hheight],
            image[0:hwidth, hheight:height],
            image[hwidth:width, hheight:height],
        ]

    return reduce(
        operator.add,
        [
            splitsingle(image)
            for image in input
        ]
    )


def blur(input, task):
    return [
        BLURRERS[task](image)
        for image in input
    ]
