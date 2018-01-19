#!/usr/bin/python

import sys
import os
import fileinput
import serial
import struct
import time

class PortTalker(object):
    def __init__(self, port):
        self.sp = serial.Serial(port, 57600)
        self.sp.setTimeout(0.02)
        self.buff = ''

    def send_picture(self, half, data):
        assert half in [0, 1]
        assert len(data) == 28
        l_bytes = [0x80, 0x83, half] + data + [0x8F]
        packed = struct.pack('32B', *l_bytes)
        self.sp.write(packed)

def make_data(filename):
    # input is a 28 line x 14 column text file consisting of '.' and 'x' characters
    # output is { 0: [ length 14 list of ints ], 1: [ same ] }
    
    d = {0: [], 1: []}
    count = 0
    for line in open(filename).readlines():
        count += 1
        if count > 28: 
            break
        line = line.replace('.', '0')
        line = line.replace('x', '1')
        bottom = line[0:7]
        top = line[7:14]
            
        d[0].append(int(top,2))
        d[1].append(int(bottom,2))

    return d

def binary_demo_tx():
    talker = PortTalker('/dev/ttyUSB0')

    ofs = 0
    while True:
        top, bottom = [], []
        pos = ofs
        for col in range(28):
            top.append(pos & 0xff)
            bottom.append((pos >> 8) & 0xff)
            pos += 1
        talker.send_picture(0, top)
        talker.send_picture(1, bottom)
        time.sleep(0.1)
        ofs += 1

def main_tx(filename):
    talker = PortTalker('/dev/ttyUSB0')
    d = make_data(filename)
    talker.send_picture(0, d[0])
    talker.send_picture(1, d[1])

        


if __name__ == '__main__':
    main_tx(sys.argv[1])
