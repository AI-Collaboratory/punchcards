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

CARD_WIDTH = 7.0 + 3.0/8.0 # Inches
CARD_HEIGHT = 3.25 # Inches
CARD_SPEC_TOLERANCE = .15  # inches, adjust as needed
CARD_W_TO_H_RATIO_HIGH = (CARD_WIDTH + CARD_SPEC_TOLERANCE) / CARD_HEIGHT
CARD_W_TO_H_RATIO_LOW = (CARD_WIDTH - CARD_SPEC_TOLERANCE) / CARD_HEIGHT

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
def normalizeFlip(orig_img, cropped_img):
    testbox = (0,0,20,20)
    brightest = -1
    test_img = cropped_img
    best_flip = (0,0)
    for (x,y), value in numpy.ndenumerate(numpy.zeros((2,2))):
        if x:
            test_img = cropped_img.transpose(Image.FLIP_LEFT_RIGHT)
        if y:
            test_img = test_img.transpose(Image.FLIP_TOP_BOTTOM)
        # test_img.show()
        b = brightness(test_img.crop(testbox))
        if b > brightest:
            brightest = b
            best_flip = (x,y)
    result = orig_img
    if best_flip[0]:
        result = result.transpose(Image.FLIP_LEFT_RIGHT)
    if best_flip[1]:
        result = result.transpose(Image.FLIP_TOP_BOTTOM)
    return result

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
    return result

# Find the index values where dark region begins and ends
def findMargins(im, axis=0, threshold=.2):
    pix = numpy.array(im)
    max = pix.shape[axis]*255
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

def combine_images( imgs ):
    imgs = [i.convert(mode="RGB") for i in imgs]
    max_width = sorted( [(i.size[0]) for i in imgs])[-1]
    imgs = [ i.resize((max_width, int(i.size[1]*max_width/i.size[0]))) for i in imgs ]
    diagnostic = numpy.vstack( imgs )
    return Image.fromarray( diagnostic, mode="RGB" )

def is_card_dimensions(image):
    card_ratio = float(image.size[0]) / float(image.size[1])
    return card_ratio <= CARD_W_TO_H_RATIO_HIGH and card_ratio > CARD_W_TO_H_RATIO_LOW

def find_card(image):
    image2 = image.convert(mode="L")
    diag = combine_images([image, image2])
    image3 = image2
    if(isnotbacklit(image2)):
        image3 = ImageOps.invert(image2)
    diag = combine_images([diag, image3])
    cropped = cropCard(image3)
    diag = combine_images([diag, cropped])
    #image.show()
    image4 = image3
    if(cropped.size[1] > cropped.size[0]):
        image4 = image3.transpose(Image.ROTATE_90)
        cropped = cropped.transpose(Image.ROTATE_90)
    if not is_card_dimensions(cropped):
        return None
    diag = combine_images([diag, image4])
    image5 = normalizeFlip(image4, cropped)
    diag = combine_images([diag, image5])
    if logger.isEnabledFor(logging.DEBUG):
        diag.show()
    return image5

if __name__ == '__main__':
    example()
