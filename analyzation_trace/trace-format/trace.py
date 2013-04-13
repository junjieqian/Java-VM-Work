#!/usr/bin/python
# trace.py
# Junjie Qian
# this file is used to calculate the trace got from read/write barriers of jikesrvm
from sys import argv
from decimal import Decimal
import string
import matplotlib.pyplot as plt

script, filename = argv

fp = open (filename, 'r')

lines = fp.readlines()

addr_list = []
time_list = []
i = 0

for line in lines:
     word = string.split(line, '\n')
     addr_list.append(int(word[0], 0))
#     print int(word[0], 0)
#     addr_list.append(Decimal(line))
     time_list.append(i)
     i += 1

plt.figure(1)
plt.plot(time_list, addr_list, 'k.')
#plt.axis([0, i, 1610000000, 1645000000]) # read barrier information
#plt.axis([0, i, 1600000000, 1900000000])
plt.axis([0, i, 1877000000, 1898000000])
#title('read barrier trace of one hashtable tuple')

plt.savefig(filename + '.png')


