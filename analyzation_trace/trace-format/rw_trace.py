#!/usr/bin/python
# rw_trace.py
# Junjie Qian
# this file is used to calculate the trace got from read and write barriers of jikesrvm, different from previous versions, this one distinguish two addresses together.
# the sample trace as "1360810779187.0010x62012160" for version with system time
# another sample trace is no system time "10x62012160" while 1 is for read operation and 0 is for write operation
from sys import argv
from decimal import Decimal
import string
import matplotlib.pyplot as plt

script, filename = argv

fp = open (filename, 'r')

lines = fp.readlines()

read_list = []
write_list = []
read_line_list = []
write_line_list = []
i = 0

for line in lines:
     word = string.split(line, '0x')
     i += 1
#     print word[0]
     if (word[0] == "1"):  # read operation
        read_list.append(int(word[1], 16))
#        print word[1]
        read_line_list.append(i)
     elif (word[0] == "0"): # write operation
        write_list.append(int(word[1], 16))
        write_line_list.append(i)


plt.figure(1)
plt.plot(read_line_list, read_list, 'k.')
plt.plot(write_line_list,write_list, 'r.')
#plt.axis([0, i, 1610000000, 1645000000]) # read barrier information
plt.axis([0, i, 1500000000, 1900000000])
#plt.axis([0, i, 1877000000, 1898000000])
#plt.axis([250, 265, 1500000000, 1898000000])
plt.title('read write accesses of hashtable example')
plt.xlabel('access time sequence')
plt.ylabel('address range')
#title('read barrier trace of one hashtable tuple')

plt.savefig(filename + '.png')


