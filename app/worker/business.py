import cv2


def resize(input, task):
    size = [int(x) for x in task.split('x')]
    return [
        cv2.resize(image, size, interpolation = cv2.INTER_AREA)
        for image in input
    ]


def split(input, task):
    def splitsingle(image):
        width, height = image.shape[:2]
        hwidth, hheight = int(width/2), int(height/2)

        slice1 = image[0:hheight, 0:]
        slice2 = image[0:hheight, 0:]
        slice3 = image[0:hheight, 0:]
        slice4 = image[0:hheight, 0:]

    return [
        splitsingle(image)
        for image in input
    ]


def blur(input, task):
    print('blurred')
