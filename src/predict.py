from __future__ import absolute_import, division, print_function

import argparse
from skimage import io
import tensorflow as tf
from img import split_letters
from model import captcha_classifier

# disable all warnings
import warnings
warnings.filterwarnings('ignore')
# disable tf runtime message
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def main(argv):

    # load image
    print('loading image:', argv)
    image = io.imread(argv, as_gray=True)

    # split into letters
    letters = split_letters(image)

    probs = []
    for i, letter in enumerate(letters):
        letter = letter.astype('float32') / 255
        predict_input_fn = tf.estimator.inputs.numpy_input_fn(
            x={'x': letter},
            y=None,
            num_epochs=1,
            shuffle=False)
        predictions = captcha_classifier.predict(input_fn=predict_input_fn)
        for pred_dict in predictions:
            class_id = pred_dict['classes']
            probs.append(str(class_id))
    print(''.join(probs))


def path():
    r = []
    base = os.path.os.getcwd() + '/data/captcha/'
    for i in os.listdir(base):
        if 'jpg' in i:
            r.append(base + i)
    return r


if __name__ == '__main__':
    for i in path():
        main(i)
