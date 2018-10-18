#!/usr/bin/python3

import os, sys
import argparse
import numpy as np
from clack import HEIGHT, WIDTH, CLACK_URL, blank_screen, read_font, clack_post
import time
# bdf library on python3 is broken
#from bdf import bdf
from getch import getche
import string

HEIGHT, WIDTH = WIDTH, HEIGHT  # we're going the other way

def banner(message, fontname='banner', fonttype='file'):
    if fonttype == 'file':
        font = read_font(fontname)
        bitmap_all = np.hstack([font[ch] for ch in message if ch in font])
    elif fonttype == 'bdf':
        b = bdf(fontname)
        bitmap_all = np.hstack([b.trim_letter(ch) for ch in message if ch in b])
    else:
        raise ValueError('fonttype must be file or bdf')

    length = np.shape(bitmap_all)[1]
    template = blank_screen(HEIGHT, length + WIDTH*2)  # blank at end and start

    # place the bitmap on the template.
    
    # how high is the image to be placed (i.e., the font)?
    fontheight = np.shape(bitmap_all)[0]
    pad = int((HEIGHT - fontheight)/2)

    if fontheight > 14:
        raise ValueError('font height max 14')
    
    template[pad:pad+fontheight, WIDTH:length+WIDTH] = bitmap_all

    return template, length


def window(template, start):
    screen = template[:, start:start+WIDTH]
    return b'\n'.join([b''.join(a) for a in np.rot90(screen, 2)])
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Show a scrolling message as you type. Ignores any characters not in the font.')
    parser.add_argument('--font', type=str, help='A BDF font file, max 14 tall.')
    args = parser.parse_args()

    if args.font:
        print("BDF fonts currently broken on Python 3.")
        sys.exit(1)

    message = ''

    while True:
        ch = getche()
        if ch not in string.printable:
            continue
        if ch == '\n':
            print("All done.")
            sys.exit(0)

        message += ch
        if len(message) > 10:
            message = message[-10:]

        if args.font:
            whole_banner, length = banner(message, args.font, 'bdf')
        else:
            whole_banner, length = banner(message)

        clack_post(window(whole_banner, length))
