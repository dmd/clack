#!/usr/bin/python3

from bdflib import reader
import numpy as np
import os, sys


class bdf:
    def __init__(self, fontfilename):
        self.bdffont = reader.read_bdf(open(fontfilename, "rb"))

    def letter(self, let):
        character = self.bdffont.glyphs_by_codepoint[ord(let)].data
        return [
            list("{0:0=8b}".format(row).replace("0", ".").replace("1", "x"))
            for row in reversed(character)
        ]

    def trim_letter(self, let):
        im = np.array(self.letter(let))
        height, width = np.shape(im)

        x_indices = np.where(im == "x")
        if len(x_indices[1]) == 0:
            return np.array(list("." * height))[:, np.newaxis]

        column_first = np.min(x_indices[1])
        column_last = np.max(x_indices[1])

        return np.hstack(
            (
                im[:, column_first : column_last + 1],
                np.array(list("." * height))[:, np.newaxis],
            )
        )
