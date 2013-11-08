# !/usr/bin/python
# inter_arrival_size.py
# Junjie Qian
# To get the inter arrival size between first write access to one object and then later access
# reason want this data is, to the memory distance between one object initialization and first use
# Input file is supposed already formatted.

from sys import argv
import string, math
import matplotlib.pyplot as plt

script, filename = argv

tracefile = open(filename, 'r')
traceline = tracefile.readlines()

object_map = {}           # hashmap used to store all the objects in the trace, it may be huge
target_lnum_map = {}      # hashmap used to store the target object address and line #
target_range_map = {}     # hashmap used to store the target object address and the address range

inter_size_list = []      # list used to store the inter sizes of different targets
target_list = []          # list of the targets for possible future use
inter_addr_list1 = []     # list of the inter addresses in Nursery
inter_addr_list2 = []     # list of the inter addresses in Mature

line_num = 0              # line number for each object
addr_range = 0
last_addr = '0'           # store the last accessed address

object_map2 = {}          # hashmap used to store all the objects in the trace, it is one backup to get next line number object address
addr_list = []            # the list used to record all the objects address, future get the addresses and index
line_num2 = 0
inter_arrival_size = 0
i = 0
j = 0
tmp = 0

for l in traceline:
    sequence = string.split(l, ' ')
    object_map2[line_num2] = sequence[2]
    line_num2 += 1
    addr_list.append(sequence[2])

for line in traceline:
    word = string.split(line, ' ')   # word[0] is the system time, word[1] is the operation mode, word[2] is the address
    object_map[word[2]] = line_num

    if (word[1] == '1') and (not target_lnum_map.has_key(word[2])):
        target_lnum_map[word[2]] = line_num                               # store the address there with the line number
        tmp = line_num
        while True:
            if (object_map2.get(tmp+1) == word[2]):
                tmp += 1
            else:
                break
        addr_range = int(object_map2[tmp], 16) - int(word[2], 16)
        target_range_map[word[2]] = addr_range

    if tmp<line_num:
#        print 'tmp, line_num', tmp, line_num
        if (target_lnum_map.has_key(word[2])) and (not word[2] == last_addr):
            del target_lnum_map[word[2]]
            del target_range_map[word[2]]
            target_list.append(word[2])
            i = tmp
            j = line_num
#            print 'i,j', i, j
            for k in range(i, j):
                if (int(addr_list[k], 16) < (1.7 * math.pow(10, 9))):
                    m = int(addr_list[k], 16)
                    inter_addr_list1.append(m)
                else:
                    n = int(addr_list[k], 16)
                    inter_addr_list2.append(n)
#               print k
#            print inter_addr_list2
            if (len(inter_addr_list1) != 0) and (len(inter_addr_list2) != 0):
                inter_arrival_size = (max(inter_addr_list1) - min(inter_addr_list1)) + (max(inter_addr_list2) - min(inter_addr_list2))
#                print max(inter_addr_list1), min(inter_addr_list1),max(inter_addr_list2), min(inter_addr_list2)
            elif (len(inter_addr_list1) == 0) and (len(inter_addr_list2) != 0):
                inter_arrival_size = (max(inter_addr_list2) - min(inter_addr_list2))
#                print max(inter_addr_list2), min(inter_addr_list2)
            elif (len(inter_addr_list1) != 0) and (len(inter_addr_list2) == 0):
                inter_arrival_size = (max(inter_addr_list1) - min(inter_addr_list1))
            elif (len(inter_addr_list1) == 0) and (len(inter_addr_list2) == 0):
                inter_arrival_size = 0
            inter_size_list.append((inter_arrival_size)/(1024*1024))
#            print inter_arrival_size
    del inter_addr_list1[:], inter_addr_list2[:]                                # clear the list
    last_addr = word[2]
    line_num += 1
#    print line_num

inter_size_sum = 0
for m in range(0, len(inter_size_list), 1):
    inter_size_sum += inter_size_list[m]
average = inter_size_sum/len(inter_size_list)

print "average inter arrival size: ", average
print "maximum inter arrival size: ", max(inter_size_list)

#result_file = open ('list_result', 'w+')
#result_file.write('inter_size: ')
#result_file.write(inter_size_list)
#result_file.write(' '.join(map(str, inter_size_list)))
#result_file.write('target list: ')
#result_file.write(target_list)
#result_file.write(' '.join(map(str, target_list)))

x = range(0, len(target_list), 1)
plt.figure(1)
plt.plot(x, inter_size_list, 'k.')
plt.axis([0, len(target_list), 0, max(inter_size_list)])
#plt.xticks(rotation=90)
#plt.xticks(x, target_list)
#plt.title('inter_arrival sizes between objects initiallization and first use')
plt.title('inter_arrival sizes')
plt.xlabel('object addresses list')
plt.ylabel('inter arrival sizes in Mega Byte')

plt.savefig(filename + '.png')


