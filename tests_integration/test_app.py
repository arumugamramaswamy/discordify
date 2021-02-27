import cv2


def get_locals():
    return repr(locals())


def add(x, y):
    return x + y


def info():
    return "Some info"


def single_print(arg):
    return arg


def to_gray(img):
    if len(img.shape) == 2:
        return img
    if img.shape[-1] == 4:
        return cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
