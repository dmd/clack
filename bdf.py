#!/usr/bin/env python2.7

from bdflib import reader
import os, sys

class bdf:
    def __init__(self, fontfilename):
        self.bdffont = reader.read_bdf(open(fontfilename))

    def letter(self, let):
        character = self.bdffont.glyphs_by_codepoint[ord(let)].data
        return [list('{0:0=8b}'.format(row).replace('0','.').replace('1','x')) for row in reversed(character)]

