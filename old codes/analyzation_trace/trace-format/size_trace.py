#!/usr/bin/python
# size_trace.py
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
#read_access_number = 1
#write_access_number = 1
#read_access_num_list = []
#write_access_num_list = []
temp_read_size = string.split(traceline, ' ')[2]  # inital starting point size, and used for size inter-arrival calculation
temp_write_size = '0x7040400c'
write_access_size = 0
read_access_size = 0
read_access_size_list = []
write_access_size_list = []
time_sequence = []

for l in tracelines:
    sequence = string.split(l, ' ')
    current_time = sequence[0]               # current time of the lines reading
    current_size = sequence[2]               # current address of the lines reading
 
    if ((Decimal(current_time)-Decimal(temp_time)) < 1):
#         temp_time = current_time
         if (sequence[1] == '0'):             # read operation
#              print current_size, temp_read_size
#              read_access_size += abs(Decimal(current_size)-Decimal(temp_read_size))
              read_access_size += abs(int(current_size,16)-int(temp_read_size, 16))
              temp_read_size = current_size
         elif (sequence[1] == '1'):             # write operation
#              write_access_size += abs(Decimal(current_size)-Decimal(temp_write_size))
              write_access_size += abs(int(current_size,16)-int(temp_write_size, 16))
              temp_write_size = current_size
    else:
         temp_time = current_time
         read_access_size_list.append(read_access_size)
         write_access_size_list.append(write_access_size)
         i += 1
         time_sequence.append(i)
         read_access_size = 0
         write_access_size = 0

plt.figure(1)
#plt.plot(time_sequence, read_access_size_list, 'k.')
plt.plot(time_sequence, write_access_size_list, 'r.')
plt.axis([0, i, 0, max(write_access_size_list)])
plt.title('access size of different time slots')
plt.xlabel('time sequence in every milliseconds')
plt.ylabel('access size')

plt.savefig(filename + '.png')
