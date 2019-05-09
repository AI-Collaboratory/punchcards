# Copyright (C) 2018: Gregory Jansen
# The code is GPL 3.0(GNU General Public License) ( http://www.gnu.org/copyleft/gpl.html )
#
"""Punch Card Reader
Usage:
  punchcard <image-file>...
  punchcard [options]

Options:
  -h --help    show this
  -v --version show program version
  -d --debug   show debug level logging
"""

from PIL import Image, ImageOps, ImageStat
import numpy
import logging
from .punchcard import PunchCard

logger = logging.getLogger('punchcard')

def example():
    example = "images/C04D01L-0001.tif"
    #example = "images/C04D01R-0033.tif"
    image = Image.open(example)
    image = image.convert(mode="L")
    if(isnotbacklit(image)):
        image = ImageOps.invert(image)
    image = cropCard(image)
    image = normalizeFlip(image)
    image.show()
    card = PunchCard(image, bright=127)
    print("Card Text:"+card.text)

# Identify the lightest corner and place it top-left
def normalizeFlip(orig_img):
    testbox = (0,0,20,20)
    brightest = -1
    test_img = orig_img
    best_flip = test_img
    for (x,y), value in numpy.ndenumerate(numpy.zeros((2,2))):
        if x:
            test_img = orig_img.transpose(Image.FLIP_LEFT_RIGHT)
        if y:
            test_img = test_img.transpose(Image.FLIP_TOP_BOTTOM)
        # test_img.show()
        b = brightness(test_img.crop(testbox))
        if b > brightest:
            brightest = b
            best_flip = test_img
    return best_flip

def cropCard(im):
    # crop along X axis
    left, right = findMargins(im, axis=0)
    # box is: L, T, R, B
    x_crop_box = (left, 0, right, im.size[1]-1)
    x_cropped = im.crop(x_crop_box)
    # x_cropped.show()

    # crop along Y axis
    top, bottom = findMargins(x_cropped, axis=1)
    y_crop_box = (0, top, x_cropped.size[0]-1, bottom)
    result = x_cropped.crop(y_crop_box)
    result.show()
    return result

# Find the index values where dark region begins and ends
def findMargins(im, axis=0, threshold=.2):
    pix = numpy.array(im)
    max = im.size[axis]*255
    max = max - int(max*threshold)
    vector = numpy.sum(pix, axis=axis)
    first = 0
    last = len(vector)-1
    #threshold = numpy.average(vector)
    #threshold = int(numpy.average(vector)/2)
    #threshold = 100
    for i in range(0, len(vector)-1):
        if(vector[i] < max):
            first = i-1
            break
    for i in range(0, len(vector)-1):
        if(vector[len(vector)-1-i] < max):
            last = len(vector)-i
            break
    return (first, last)


# Determine if card is darker than the background
def isnotbacklit(image):
    # is the center lighter or darker than the edges..
    # pick a center square and avg brightness
    width, height = image.size
    ctr_box = (width/4, height/4, (width/4)*3, (height/4)*3)
    ctr_region = image.crop(ctr_box)
    # pick square left edge to center square and avg brightness.
    left_box = (0, height/4, width/4, (height/4)*3)
    left_region = image.crop(left_box)
    return brightness(left_region) < brightness(ctr_region)

def brightness( im ):
    stat = ImageStat.Stat(im)
    return stat.mean[0]

def find_card(image):
    image = image.convert(mode="L")
    if(isnotbacklit(image)):
        image = ImageOps.invert(image)
    image = cropCard(image)
    #image.show()
    if(image.size[1] > image.size[0]):
        image = image.transpose(Image.ROTATE_90)
    image = normalizeFlip(image)
    return image

if __name__ == '__main__':
    example()
