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
    card = PunchCard(im, bright=127, debug=False)
    print(card.text)
  else:
    print('Not a punchcard.')

def test_cards():
    card_images = [f for f in listdir('images/') if isfile(join('images/', f))]
    for name in card_images:
        testcard(join('images/', name))

def test_noncards():
    non_card_images = [f for f in listdir('images/not_punchcards/') if isfile(join('images/not_punchcards/', f))]
    for name in non_card_images:
        testcard(join('images/not_punchcards/', name))

def test_examples():
    files = [
        'images/C04D01L-0001.tif',
        'images/C04D01L-0001-90.tif',
        'images/C04D01L-0001-big-canvas.png',
        'images/C04D01L-0001-cropped-tight.tif',
        'images/sample.png',
    ]
    text = 'MACON FORT                       4628      NORTH CAROLINA                        '
    for file in files:
        result = read_card(file)
        if not(result == text):
            print("Read errors for {0}".format(file))
            image = Image.open(file)
            image.show()
        assert result == text

if __name__ == "__main__":
    test_cards()
    test_noncards()
