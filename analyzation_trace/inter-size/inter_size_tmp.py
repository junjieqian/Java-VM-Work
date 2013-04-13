#!/usr/bin/python
# inter_size_trace.py
# Junjie Qian
# this file is used to calculate the trace got from read and write barriers of jikesrvm, this one distinguish two addresses together.
# this file first converts to the standard trace formate, 
# then calculates the inter-arrival size between the initialization and first use of the object.
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

############# new format trace file generated #########

tracefile = open('trace2', 'r')
#traceline = tracefile.readline()
tracelines = tracefile.readlines()
tracefile.close()

inter_size = 0                    # inter size between one object
inter_size_list = []              # array to store the future inter-arrival sizes between same object initialization and use
object_list = []                  # array to store the objects
destin_list = []                  # arrary to store the initilial and first use objects
i = 0
j = 0
k = 0

with open('trace2', 'rb') as f:
  for l in iter(f.readline, ""):
    sequence = string.split(l, ' ')
    i += 1

    if (sequence[1] == '1'):
        current_address = sequence[2]
        next_address = sequence[2]
        print current_address
        for temp_line in iter(f.readline, ''):
            temp_sequence = string.split(temp_line, ' ')
            if(temp_sequence[2] != next_address):
                next_address = temp_sequence[2]
                break

        for temp_line2 in iter(f.readline, ''):
            temp_sequence2 = string.split(temp_line2, ' ')
            if (temp_sequence2[2] >= current_address) and (temp_sequence2[2] <= current_address):
                break
            else:
                object_list.append(temp_sequence2[2])



        if (len(object_list) == 0):
            inter_size = 0
        else:
            print object_list, "max and min"
            inter_size = int(max(object_list), 16) - int(min(object_list), 16)

        print  current_address, next_address, inter_size, "!!addresses !!"
        inter_size_list.append(inter_size)
        destin_list.append(current_address)
        inter_size = 0
        j = 0
        k = 0
        del object_list[0:len(object_list)]



#plt.figure(1)
#plt.plot(destin_list, inter_size_list, 'k.')
#plt.plot(time_sequence, write_access_num_list, 'r.')
#plt.axis([0, len(destin_list), 0, 2500])
#plt.title('inter_arrival sizes between objects initiallization and first use')
#plt.xlabel('object addresses list')
#plt.ylabel('inter_arrival sizes')

#plt.savefig(filename + '.png')




