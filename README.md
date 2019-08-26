# Punch Card Reader

This is a Python module to interpret the string encoded on a IBM 80 column standard punch card. It was originally written in 2011 by Michael Hamilton with a GPL license, which carries forward to this open source code. We are adapting this code to make it
serve more broad use cases, adding image detection and normalization steps prior
to the card interpretation:

## Processing Steps:
1. Convert image to black and white. (8bit grayscale, array of values from 0 to 255)
1. Find out if card is backlit or not. (white card or black card , black holes or white holes)
1. Invert image colors if needed to get a black card with white holes.
1. Find the card crop region by looking at X and Y axis brightness summations.
1. Verify punch card image based on crop region proportions. Is this an IBM card?
1. Detect the missing corner and flip card image to place it top-left.
1. Call existing Michael Hamilton's adapted PunchCard class.

## Installation
1. Install Python 2.x and PIP. (https://wiki.python.org/moin/BeginnersGuide/Download)
1. Using PIP, install the `punchcards` package:
```
$ pip install punchcards
```
If you like, you can add the --user flag to reduce the permissions needed to install. You could
also use a Python virtual environment.
1. Now make sure that the `punchcards` command is on your path:
```
$ punchcards -h
Usage:
  punchcard <image-file> ...
  punchcard (-h | --help)
  punchcard --version
```
You should see the usage text printed to your console, as above.
1. If you need to process TIFF format images, you ~may~ need to install the `libtiff` package for your system. Please see
the details on the [Pillow site](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html?highlight=tiff#tiff).

## Example Usage
Say you have a collection of punchcard scans or isometric digital photos, you can
call the `punchcards` command to parse the text encoded on the cards. The card must
be centered in your images and the image must be relatively high contrast (dark on light, or
light on dark) to clearly show the missing 'chads' or punch holes.

If your images are together in a folder, you can run the command as follows:
```
$ cd punchcard_images
$ punchcards *
```
You should then see the text on each card printed to your console.

## Using the API in Python
The recommended API in this module consists of one core function (`find_card`) and one core
class (`PunchCard`). The punchcards module uses the Image class from the Pillow
version of the Python Image Library (PIL).
In this example code, you can see how these are used together to read card text:
```python
from PIL import Image
from punchcards.normalize import find_card
from punchcards.punchcard import PunchCard
from os import listdir
from os.path import isfile, join

def testcard( filepath ):
  print(filepath)
  im = Image.open(filepath)
  im = find_card(im)
  if im is not None:
    card = PunchCard(im)
    print(card.text)
  else:
    print('Not a punchcard.')
```

The find_card function normalizes a punchcard image for rotation, flip, and backlit.
It returns a derived image that is suitable for the PunchCard class or None. The PunchCard
class knows how to find and interpret the pattern of holes in card images as text.
You can also use the PunchCard class to generate an image of a card with text of
your choosing.
