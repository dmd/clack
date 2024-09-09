#!/usr/bin/python3

import numpy as np
import os
from glob import glob
import requests

WIDTH, HEIGHT = 14, 28
CLACK_URL = 'http://your-clack-host:8080/clack/'


def blank_screen(height=HEIGHT, width=WIDTH):
    """ a blank matrix """
    d = np.zeros((height, width), dtype='|S1')
    d[:] = '.'
    return d


def read_font(fontname):
    """ a dict of symbol bitmaps """

    font = {}
    fontdir = os.path.dirname(os.path.realpath(__file__)) + '/font/'
    symbol_files = glob(fontdir + fontname + '/*')
    for symbol_file in symbol_files:
        if os.path.basename(symbol_file) == 'SPACE':
            symbol = ' '
        else:
            symbol = os.path.basename(symbol_file)
        if symbol.startswith('u_'):
            symbol = symbol[-1]
        font[symbol] = np.array([list(x) for x in np.loadtxt(symbol_file, dtype='str')])
    return font


def clack_post(screen):
    """ send a screen to the clack """

    requests.post(CLACK_URL, data={'bitmap': screen})
