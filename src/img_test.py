from __future__ import print_function, absolute_import, division
from math import floor, ceil
from skimage import img_as_ubyte
from skimage.measure import find_contours
from skimage.util import crop
from skimage.transform import resize

# import matplotlib.pyplot as plt

SHIFT_PIXEL = 3  # shift image from right to left
BINARY_THRESH = 30  # image binary thresh
LETTER_SIZE = (12, 10)  # letter width, heigth


def split_letters(image, num_letters=4, debug=False):
    """
    split full captcha image into `num_letters` lettersself.
    return list of letters binary image (0: white, 255: black)
    """

    # move left
    left = crop(image, ((0, 0), (0, image.shape[1] - SHIFT_PIXEL)), copy=True)
    image[:, :-SHIFT_PIXEL] = image[:, SHIFT_PIXEL:]
    image[:, -SHIFT_PIXEL:] = left

    # binarization
    binary = image > BINARY_THRESH

    letter_boxs = [[[0, 5], [10, 17]], [[9, 5], [19, 17]], [[18, 5], [28, 17]], [[27, 5], [37, 17]]]

    letters = []
    for [x_min, y_min], [x_max, y_max] in letter_boxs:
        letter = resize(image[y_min:y_max, x_min:x_max], LETTER_SIZE)
        letter = img_as_ubyte(letter < 0.6)
        letters.append(letter)

    return letters
