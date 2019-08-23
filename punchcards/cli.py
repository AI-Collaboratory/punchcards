#!/usr/bin/env python
from .punchcard import PunchCard
from .normalize import find_card
from PIL import Image
from docopt import docopt
import logging

__doc_opt__ = """Punchcard Command Line Interface.

Usage:
  punchcard <image-file> ...
  punchcard (-h | --help)
  punchcard --version
"""

if __name__ == '__main__':
    main()

def main():
    args = docopt(__doc_opt__, version='Punch Card Reader 1.0')

    logger = logging.getLogger('punchcard')
    logger.setLevel(logging.WARN)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if '--debug' in args:
        logger.setLevel(logging.DEBUG)

    for item in args['<image-file>']:
        im = Image.open(item)
        im = find_card(im)
        if im is not None:
            card = PunchCard(im, bright=127, debug=False)
            print(card.text)
        else:
            print('Not a punchcard.')
