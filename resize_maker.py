from PIL import Image
from os import path

image_width, image_height = 512, 512


def resize(infile):
    file, ext = path.splitext(infile)
    with Image.open(infile) as im:
        new_img = im.resize((image_width, image_height), Image.ANTIALIAS)
        # new_img.mode = 'RBG'
        new_img.save(file + '_resized.jpg', 'JPEG')


if __name__ == '__main__':

    resize('image_folder/solar_system.jpg')