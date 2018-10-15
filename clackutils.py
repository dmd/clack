#!/usr/bin/python3

from __future__ import print_function
import os, sys
from datetime import datetime
from clack import *


def counter(n):
    """ draw the CSA numerical counter """

    str_n = str(n).rjust(2, '_')
    font = read_font('7')
    screen = blank_screen(height=7, width=WIDTH)

    screen[0:7, 2:7] = font[str_n[0]]
    screen[0:7, 8:13] = font[str_n[1]]
    return screen


def clock():
    """ draw a clock """
    font = read_font('5ext')
    screen = blank_screen(height=5, width=WIDTH)
    d = datetime.now()
    hour = str(int(d.strftime('%I')))
    minutes = d.strftime('%M')
    min10 = minutes[0]
    min1 = minutes[1]

    if len(hour) == 2:
        screen[0:5, 0:5] = font[hour]
    else:
        screen[0:5, 1:4] = font[hour]
        # colon
        screen[1, 5] = 'x'
        screen[3, 5] = 'x'

    screen[0:5, 7:10] = font[min10]
    screen[0:5, 11:14] = font[min1]
    return screen

