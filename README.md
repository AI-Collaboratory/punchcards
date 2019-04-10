# Punch Card Reader

This is a Python module to interpret the string encoded on a IBM 80 column standard punch card. It was originally written in 2011 by Michael Hamilton with a GPL license, which
carries forward to this open source code. We are adapting this code to make it
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

## TODO
* Has trouble cropping this image file vertically:
```
from punchcards import read_card
>>> print(read_card('images/C04D01L-0001.tif'))
```
* Needs testing as a package, clearer API
