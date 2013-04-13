#!/usr/bin/python
# time_trace.py
# Junjie Qian
# this file is used to calculate the trace got from read and write barriers of jikesrvm, different from previous versions, this one distinguish two addresses together.
# the sample trace as "1360810779187.0010x62012160" for version with system time
# another sample trace is no system time "10x62012160" while 0 is for read operation and 1 is for write operation
from sys import argv
from decimal import Decimal
import string
import matplotlib.pyplot as plt

script, filename = argv

fp = open (filename, 'r')
f = open('trace2', 'w+')

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

fp.close()
f.close()

tracefile = open('trace2', 'r')
traceline = tracefile.readline()
tracelines = tracefile.readlines()
tracefile.close()

i = 0
temp_time = string.split(traceline, ' ')[0]  # inital starting point time, and used for time inter-arrival calculation
#tmp = temp_time                              # used for future total time increment calculation
read_access_number = 1
write_access_number = 1
read_access_num_list = []
write_access_num_list = []
time_sequence = []

for l in tracelines:
    sequence = string.split(l, ' ')
    current_time = sequence[0]               # current time of the lines reading
    
    if ((Decimal(current_time)-Decimal(temp_time)) < 101):
#    if ((Decimal(current_time)-Decimal(temp_time)) < 101):     # < ? stands for how many milliseconds
#         temp_time = current_time
         if (sequence[1] == '0'):             # read operation
              read_access_number += 1
         elif (sequence[1] == '1'):             # write operation
              write_access_number += 1
    else:
         temp_time = current_time
         read_access_num_list.append(read_access_number)
         write_access_num_list.append(write_access_number)
         i += 1
         time_sequence.append(i)
         read_access_number = 0
         write_access_number = 0

plt.figure(1)
plt.plot(time_sequence, read_access_num_list, 'k.')
plt.plot(time_sequence, write_access_num_list, 'r.')
plt.axis([0, i, 0, 2500])
plt.title('access numer of different time slots')
plt.xlabel('time sequence in every 100 milliseconds')   # change the xlable if needed
plt.ylabel('access number')

plt.savefig(filename + '.png')
