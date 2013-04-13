#!/usr/bin/python
# trace_format2.py
# Junjie Qian
# this file is used to calculate the trace got from read and write barriers of jikesrvm, different from previous versions, this one distinguish two addresses together.
# this file first converts to the standard trace formate, then calculates the access frequency according to system time flows.
# the sample trace as "1361422111014 (0x0000013cfb14d126)00x620191d40x00000040" for version with system time
# another sample trace is no system time "10x62012160" while 0 is for read operation and 1 is for write operation
from sys import argv
from decimal import Decimal
import string
import matplotlib.pyplot as plt

script, filename = argv

fp = open (filename, 'r')
f = open('trace_new', 'w+')

lines = fp.readlines()

for line in lines:
    word1 = string.split(line, ' ')
    f.write(word1[0])  # system time
    f.write(' ')
    word2 = string.split(word1[1], ')')
    word3 = string.split(word2[1], '0x')
    f.write(word3[0])  # read/write operation tag
    f.write(' ')
    f.write('0x' + word3[1])  # address information
    f.write(' ')
    f.write('0x' + word3[2])  # offset

fp.close()
f.close()
