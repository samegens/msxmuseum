#!/usr/bin/python

from PIL import Image
from PIL import ImageFile
import os
import shutil


def ScaleToMax(inOldWidth, inOldHeight, inMaxWidth, inMaxHeight):
    width_scale = float(inMaxWidth) / float(inOldWidth)
    height_scale = float(inMaxHeight) / float(inOldHeight)
    scale = min(width_scale, height_scale)
    return (int(inOldWidth * scale), int(inOldHeight * scale))


for root, dirnames, filenames in os.walk('.'):
    for filename in filenames:
        if filename.endswith('boxshot.jpg'):
            path = os.path.join(root, filename)
            print('Found boxshot %s' % os.path.join(root, filename))
            img = Image.open(path)
            width, height = img.size
            print('  width = %d, height = %d' % (width, height))
            if width != 212 and height != 300:
                shutil.copyfile(path, path + '.org')
                new_width, new_height = ScaleToMax(width, height, 212, 300)
                print('  needs resize, new width = %d, new height = %d' % (new_width, new_height))
                img = img.resize( (new_width, new_height), Image.ANTIALIAS)
                img.save(path, "JPEG", quality=80)
            else:
                print('  OK')
        if filename.endswith('screenshot.png'):
            path = os.path.join(root, filename)
            print('Found screenshot %s' % os.path.join(root, filename))
            img = Image.open(path)
            width, height = img.size
            print('  width = %d, height = %d' % (width, height))
            if width != 320 and height != 240:
                shutil.copyfile(path, path + '.org')
                new_width, new_height = ScaleToMax(width, height, 320, 240)
                print('  needs resize, new width = %d, new height = %d' % (new_width, new_height))
                img = img.resize( (new_width, new_height))
                img.save(path, "PNG")
            else:
                print('  OK')
            

