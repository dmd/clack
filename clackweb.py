#!/usr/bin/python

from numpy import rot90, array
import sys
import os
import fileinput
import serial
import struct
import time
from flask import Flask, request, jsonify

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

def make_data_from_file(filename):
    return make_data(open(filename).readlines())

def make_data(lines):
    # input is a 28 line x 14 column text file consisting of spaces and x
    # output is ( [ length 14 list of ints ], [ same ] )
    
    d = ([], [])
    count = 0
    for line in lines:
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

def display_write(lines):
    talker = PortTalker('/dev/ttyUSB0')
    d = make_data(lines)
    talker.send_picture(0, d[0])
    talker.send_picture(1, d[1])

def rotate(arr):
    line2d = [list(row) for row in arr]
    rotated = rot90(array(line2d))
    return [''.join(row) for row in rotated]

app = Flask(__name__)

@app.route('/clack/', methods=['POST'])
def clack_set():
    """ send a new bitmap to the display """

    bitmap = request.form['bitmap'].split('\n')

    # is it wide? rotate.
    if len(bitmap[0]) == 28:
        bitmap = rotate(bitmap)

    display_write(bitmap)
    return jsonify(status='success')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
    
