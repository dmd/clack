#!/usr/bin/env python2.7

import numpy as np
import os
from glob import glob
import requests


WIDTH, HEIGHT = 14, 28

CLACK_URL = 'http://your-clackweb-host:8080/clack/'

def blank_screen(height=HEIGHT, width=WIDTH):
    """ a blank matrix """
    d = np.zeros((height, width), dtype='|S1')
    d[:] = '.'
    return d


def read_font(fontname):
    """ a dict of symbol bitmaps """

    font = {}
    symbol_files = glob('font/' + fontname + '/*')
    for symbol_file in symbol_files:
        symbol = os.path.basename(symbol_file)
        font[symbol] = np.array([list(x) for x in np.loadtxt(symbol_file, dtype='string')])
    return font


def clack_post(screen):
    """ send a screen to the clack """

    requests.post(CLACK_URL, data={'bitmap': screen})


