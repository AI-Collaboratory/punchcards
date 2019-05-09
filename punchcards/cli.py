from .punchcard import PunchCard
from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__, version='Punch Card Reader 1.0')

    logger = logging.getLogger('punchcard')
    logger.setLevel(logging.WARN)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if '--debug' in args:
        logger.setLevel(logging.DEBUG)

    for item in args['<image-file>']:
        image = Image.open(item)
        image.show()
        image = find_card(image)
        image.show()
        card = PunchCard(image, bright=127) # using neutral gray as threshold color
        return card.text
