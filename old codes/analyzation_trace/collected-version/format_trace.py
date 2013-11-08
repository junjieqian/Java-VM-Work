#!/usr/bin/python
# format_trace.py
# Junjie Qian
# this version is designed for large trace log file, first change 03.10.2013

# this file is used to calculate the trace got from read and write barriers of jikesrvm, different from previous versions, this one distinguish two addresses together.
# this file first converts to the standard trace formate, then calculates the access frequency according to system time flows.
# the sample trace as "1361422111014 (0x0000013cfb14d126)24000x620191d40x00000040" for version with system time
# another sample trace is no system time "10x62012160" while 0 is for read operation and 1 is for write operation
from sys import argv
from decimal import Decimal
import string
import matplotlib.pyplot as plt

script, filename = argv

fp = open (filename, 'r')
f = open(filename+'_new', 'w+')
i = 0
#lines = fp.readlines()

#for line in lines:
for line in fp:
    try:
        word1 = string.split(line, ' ')
        f.write(word1[0])         # system time
        f.write(' ')
        word2 = string.split(word1[1], ')')
        word3 = string.split(word2[1], '0x')
        f.write(word3[0][-1])     # read/write operation tag
        f.write(' ')
        word4 = string.split(word3[2], '\n')
 
        if (int(word3[1],16)+int(word4[0],16)) > int('0xffffffff',16):
            f.write(hex((int(word3[1],16)+int(word4[0],16)) - int('0x100000000',16)))
        else:
            f.write(hex((int(word3[1],16)+int(word4[0],16))))
        f.write(' ')

        f.write('123')             # this is only for matching the previous format to use the source code
        f.write(' ')

        if (int(word4[0],16)>int('0xffff0000',16)):
            f.write(str(int('0x100000000',16)-int(word4[0],16)))
        else:
            f.write(str(int(word3[0][:-1], 0)-int(word4[0],16)))
        f.write('\n')
    except:
        print i
    i += 1

fp.close()
f.close()
