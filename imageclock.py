#!/usr/bin/env python3

from __future__ import print_function
import numpy as np
import os, sys
import traceback
from clack import *
from clackutils import clock

CLACKDIR = os.path.dirname(os.path.realpath(__file__))
ERROR = open(CLACKDIR + '/error.txt').read()

def create_display(rotate=False, image='none'):
    """ generate the output for posting to the clack """

    screen = blank_screen()

    imagefont = read_font('img')[image]
    screen[0:22,:] = imagefont

    # place the clock
    screen[HEIGHT-5:HEIGHT, 0:WIDTH] = clock()

    if rotate:
        screen[:14, :] = np.rot90(screen[:14, :], 3)
        screen[14:, :] = np.rot90(screen[14:, :], 3)
    return b'\n'.join([b''.join(a) for a in screen]), screen


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Show image with clock.')
    parser.add_argument('--rotate', dest='rotate', action='store_true')
    parser.add_argument('--image', type=str, help='22 line font image.')
    args = parser.parse_args()

    try:
        d, d_arr = create_display(args.rotate, args.image)
        print ("Created display ok.")
        if args.rotate:
            print (b'\n'.join([b''.join(a) for a in np.rot90(d_arr)]))

        else:
            print (d.decode('ascii'))
    except Exception as err:
        print ('{}: {}'.format(type(err), err))
        traceback.print_exc(file=sys.stdout)
        clack_post(ERROR)
        print ('error')
        sys.exit(1)

    clack_post(d)


