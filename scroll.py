#!/usr/bin/env python2.7

import os, sys
import argparse
from glob import glob
import requests
import numpy
from clack import HEIGHT, WIDTH, CLACK_URL, blank_screen, read_font, clack_post
import time
from bdf import bdf

HEIGHT, WIDTH = WIDTH, HEIGHT  # we're going the other way

def banner(message, fontname='banner', fonttype='file'):
    if fonttype == 'file':
        font = read_font(fontname)
        bitmap_all = numpy.hstack([font[ch] for ch in message])
    elif fonttype == 'bdf':
        b = bdf(fontname)
        bitmap_all = numpy.hstack([b.letter(ch) for ch in message])
    else:
        raise ValueError('fonttype must be file or bdf')

    length = numpy.shape(bitmap_all)[1]
    template = blank_screen(HEIGHT, length + WIDTH*2)  # blank at end and start

    # place the bitmap on the template.
    
    # how high is the image to be placed (i.e., the font)?
    fontheight = numpy.shape(bitmap_all)[0]
    pad = int((HEIGHT - fontheight)/2)

    if fontheight > 14:
        raise ValueError('font height max 14')
    
    template[pad:pad+fontheight, WIDTH:length+WIDTH] = bitmap_all

    return template, length


def window(template, start):
    screen = template[:, start:start+WIDTH]
    return '\n'.join([''.join(a) for a in screen])
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Show a scrolling message.')
    parser.add_argument('--font', type=str, help='A BDF font file, max 14 tall.')
    parser.add_argument('message', type=str, help='The (quoted) message.')
    args = parser.parse_args()

    if args.font:
        whole_banner, length = banner(args.message, args.font, 'bdf')
    else:
        whole_banner, length = banner(args.message)

    for i in range(length + WIDTH):
        screen = window(whole_banner, i)
        time.sleep(0.05)
        clack_post(screen)


