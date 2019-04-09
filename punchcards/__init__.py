# Copyright (C) 2018: Gregory Jansen
# The code is GPL 3.0(GNU General Public License) ( http://www.gnu.org/copyleft/gpl.html )
#
"""Punch Card Reader
Usage:
  punchcard.py <image-file>...
  punchcard.py [options]

Options:
  -h --help    show this
  -v --version show program version
"""

from .punchcard import PunchCard
from docopt import docopt
from PIL import Image, ImageOps, ImageStat
import numpy

def example():
    example = "images/C04D01L-0001.tif"
    #example = "images/C04D01R-0033.tif"
    image = Image.open(example)
    image = image.convert(mode="L")
    if(isnotbacklit(image)):
        image = ImageOps.invert(image)
    #image.show()
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
    pix = numpy.array(im)
    v_sums = numpy.sum(pix, axis=0)
    top, bottom = findMargins(v_sums)
    h_sums = numpy.sum(pix, axis=1)
    left, right = findMargins(h_sums)
    box = (top, left, bottom, right)
    return im.crop(box)

# Find the index values where dark region begins and ends
def findMargins(vector):
    first = -1
    last = -1
    avg = numpy.average(vector)
    for i in range(0, len(vector)):
        if(vector[i] < avg):
            first = i-1
            break
    for i in range(0, len(vector)):
        if(vector[len(vector)-i-1] < avg):
            last = len(vector)-i+1
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

def read_card(image_file):
    image = Image.open(image_file)
    image = image.convert(mode="L")
    if(isnotbacklit(image)):
        image = ImageOps.invert(image)
    image = cropCard(image)
    if(image.size[1] > image.size[0]):
        image = image.transpose(Image.ROTATE_90)
    image = normalizeFlip(image)
    image.show()
    card = PunchCard(image, bright=127)
    return card.text

if __name__ == '__main__':
    args = docopt(__doc__, version='Punch Card Reader 1.0')
    for item in args['<image-file>']:
        print(read_card(item))
