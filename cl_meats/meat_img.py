#!/usr/bin/python2
# -*- coding: utf-8 -*-
from PIL import Image
import sys
import time
import base64
import StringIO

character = u'▄'
native = "_xterm256.c"

CUBE_STEPS = [0x00, 0x5F, 0x87, 0xAF, 0xD7, 0xFF]
BASIC16 = ((0, 0, 0), (205, 0, 0), (0, 205, 0), (205, 205, 0),
           (0, 0, 238), (205, 0, 205), (0, 205, 205), (229, 229, 229),
           (127, 127, 127), (255, 0, 0), (0, 255, 0), (255, 255, 0),
           (92, 92, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255))

def xterm_to_rgb(xcolor):
    assert 0 <= xcolor <= 255
    if xcolor < 16:
        # basic colors
        return BASIC16[xcolor]
    elif 16 <= xcolor <= 231:
        # color cube
        xcolor -= 16
        return (CUBE_STEPS[(xcolor / 36) % 6],
                CUBE_STEPS[(xcolor / 6) % 6],
                CUBE_STEPS[xcolor % 6])
    elif 232 <= xcolor <= 255:
        # gray tone
        c = 8 + (xcolor - 232) * 0x0A
        return (c, c, c)

COLOR_TABLE = [xterm_to_rgb(i) for i in xrange(256)]

def rgb_to_xterm(r, g, b):
    if r < 5 and g < 5 and b < 5:
        return 16
    best_match = 0
    smallest_distance = 10000000000
    for c in xrange(16, 256):
        d = (COLOR_TABLE[c][0] - r) ** 2 + \
            (COLOR_TABLE[c][1] - g) ** 2 + \
            (COLOR_TABLE[c][2] - b) ** 2
        if d < smallest_distance:
            smallest_distance = d
            best_match = c
    return best_match

def printPixels(rgb1,rgb2):
    c1 = rgb_to_xterm(rgb1[0], rgb1[1],rgb1[2])
    c2 = rgb_to_xterm(rgb2[0], rgb2[1],rgb2[2])
    sys.stdout.write('\x1b[48;5;%d;38;5;%dm' % (c1, c2))
    sys.stdout.write(character)

def printImage(im, width, height):
    for y in range(0,height-1,2):
        for x in range(width):
            p1 = im.getpixel((x,y))
            p2 = im.getpixel((x,y+1))
            printPixels(p1, p2)
        print('\x1b[0m')

def iterateImages(im):

    while True:
        printImage(getFrame(im))
        try:
            im.seek(im.tell()+1)
        except EOFError:
            break

def getFrame(im, orig_width, orig_height, width, height):
        if width!=orig_width or height!=orig_height:
            return im.resize((width,height), Image.ANTIALIAS).convert('RGB')
        else:
            return im.convert('RGB')

def compile_speedup():
    
    import os
    import ctypes
    
    from os.path import join, dirname, getmtime, exists, expanduser
    
    # library = join(dirname(__file__), '_xterm256.so')
    library = expanduser('~/.xterm256.so')
    sauce = join(dirname(__file__), native)

    if not exists(library) or getmtime(sauce) > getmtime(library):
        build = "gcc -fPIC -shared -o %s %s" % (library, sauce)
        assert os.system(build + " >/dev/null 2>&1") == 0

    xterm256_c = ctypes.cdll.LoadLibrary(library)
    xterm256_c.init()
    
    def xterm_to_rgb(xcolor):
        res = xterm256_c.xterm_to_rgb_i(xcolor)
        return ((res >> 16) & 0xFF, (res >> 8) & 0xFF, res & 0xFF)

    return (xterm256_c.rgb_to_xterm, xterm_to_rgb)

def meat_img(b64_gif, debug, width=20, height=14):
    
    # format string
    b64_gif = b64_gif.split('base64,')[1]

    # pad string
    b64_gif += "=" * ((4 - len(b64_gif) % 4) % 4)

    # decode string
    data = base64.b64decode(b64_gif)

    # read in encoded data
    f = StringIO.StringIO(data)
    
    # get original height and width
    im = Image.open(f)
    orig_width = im.size[0]
    orig_height = im.size[1]
    
    # try to speedup compiling
    try:
        (rgb_to_xterm, xterm_to_rgb) = compile_speedup()
    except:
        if debug:
            print("Failed to compile code, no speedup")

    frame = getFrame(im, orig_width, orig_height, width, height)
    printImage(frame, width, height)   


