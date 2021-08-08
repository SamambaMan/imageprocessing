import cv2


def gaussian(image):
    return cv2.GaussianBlur(image, (5, 5), 0)


def updownsampling(image):
    return cv2.pyrUp(
        cv2.pyrDown(
            image
        )
    )


def bilateral(image):
    return cv2.bilateralFilter(image, 9, 75, 75)


def median(image):
    return cv2.medianBlur(image, 5)


BLURRERS = {
    'gaussian': gaussian,
    'updownsampling': updownsampling,
    'bilateral': bilateral,
    'median': median,
}
