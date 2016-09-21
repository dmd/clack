#!/usr/bin/env python2.7

import os, sys
from glob import glob
import requests
import numpy
from clack import HEIGHT, WIDTH, CLACK_URL, blank_screen, read_font, clack_post
import time

HEIGHT, WIDTH = WIDTH, HEIGHT  # we're going the other way

def banner(message, fontname='banner'):
    font = read_font(fontname)
    bitmap_all = numpy.hstack([font[ch] for ch in message])

    length = numpy.shape(bitmap_all)[1]
    template = blank_screen(HEIGHT, length + WIDTH*2)  # blank at end and start

    # place the bitmap on the template.
    # the bitmap is 8 tall, so 3 8 3 to make 14
    template[3:11, WIDTH:length+WIDTH] = bitmap_all

    return template, length


def window(template, start):
    screen = template[:, start:start+WIDTH]
    return '\n'.join([''.join(a) for a in screen])
    

if __name__ == '__main__':
    message = sys.argv[1]
    whole_banner, length = banner(message)

    for i in range(length + WIDTH):
        screen = window(whole_banner, i)
        time.sleep(0.05)
        clack_post(screen)


