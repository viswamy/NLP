'''
@author: Virupaksha Swamy
@email: vswamy@usc.edu
@description: Program to convert UTF16 to UTF8
'''

import sys

input_file = open(sys.argv[1],"rb")
output_file = open("utf8encoder_out.txt", "wb")

iter = 0
out = bytearray()

while(True):
    data = input_file.read(2)
    if(len(data) == 0):
        break
    x = data[1]
    x = x + (data[0] << 8)
    if(x >= 0 and x <= 127):
        fb = data[1]
        out.append(fb)
        continue
    elif(x >= 128 and x <= 2047):
        sb = 0b10000000 | (x & 0b00000111111)
        fb = 0b11000000 | ((x & 0b11111000000) >> 6)
        out.append(fb)
        out.append(sb)
        continue
    elif(x >= 2048 and x <= 65535):
        tb = 0b10000000 | (x & 0b0000000000111111)
        sb = 0b10000000 | ((x & 0b0000111111000000) >> 6)
        fb = 0b11100000 | ((x & 0b1111000000000000) >> 12)
        out.append(fb)
        out.append(sb)
        out.append(tb)
    
output_file.write(out)
