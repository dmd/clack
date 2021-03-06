#!/usr/bin/python3

import random
import sys
import os
import fileinput
import serial
import struct
import time

class PortTalker(object):
    def __init__(self, port):
        self.sp = serial.Serial(port, 57600, timeout=0.02)
        self.buff = ''

    def send_picture(self, half, data):
        assert half in [0, 1]
        assert len(data) == 28
        l_bytes = [0x80, 0x83, half] + data + [0x8F]
        packed = struct.pack('32B', *l_bytes)
        self.sp.write(packed)

def blackwhite_tx():
    talker = PortTalker('/dev/ttyUSB0')

    ofs = 0
    while True:
        top, bottom = [], []
        for col in range(28):
            top.append(127)
            bottom.append(0)

        talker.send_picture(0, top)
        talker.send_picture(1, bottom)
        time.sleep(0.1)
        talker.send_picture(0, bottom)
        talker.send_picture(1, top)
        time.sleep(0.1)




if __name__ == '__main__':
    blackwhite_tx()
