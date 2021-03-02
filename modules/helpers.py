from pygame import image as pyimage
from pygame import quit
from sys import exit

from settings import MEDIA_PATH


def load_image(filename, colorkey=None):
    file_path = MEDIA_PATH / filename

    image = pyimage.load(file_path)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image


def terminate():
    quit()
    exit()
