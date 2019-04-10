
def test_examples():
    from PIL import Image
    from punchcards import read_card
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
