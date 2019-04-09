
def test_examples():
    from PIL import Image
    from punchcards import read_card
    text = 'MACON FORT                       4628      NORTH CAROLINA                        '
    assert read_card('images/C04D01L-0001.tif') == text
    assert read_card('images/C04D01L-0001-90.tif') == text
    assert read_card('images/C04D01L-0001-big-canvas.png') == text
    assert read_card('images/C04D01L-0001-cropped-tight.tif') == text
    assert read_card('images/sample.png') == text
