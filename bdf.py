#!/usr/bin/env python2.7

from bdflib import reader
import numpy as np
import os, sys

class bdf:
    def __init__(self, fontfilename):
        self.bdffont = reader.read_bdf(open(fontfilename))

    def letter(self, let):
        character = self.bdffont.glyphs_by_codepoint[ord(let)].data
        return [list('{0:0=8b}'.format(row).replace('0','.').replace('1','x')) for row in reversed(character)]

    def trim_letter(self, let):
        im = np.array(self.letter(let))

        height, width = np.shape(im)

        # find the first and last column with a black pixel
        # np.where or something like that would probably work better but who cares
        for column_first in range(width):
            if 'x' in im[:, column_first]:
                break

        for column_last in reversed(range(width)):
            if 'x' in im[:, column_last]:
                break

        assert(column_last + 1 <= width)
        return np.hstack((im[:, column_first:column_last+1],np.array(list('.' * height))[:, np.newaxis]))


