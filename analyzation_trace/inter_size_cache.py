# inter_size_large.py
# Junjie Qian
# this version is for large trace file, 03.11.2013
# To get the inter arrival size between first write access to one object and then later access
# reason want this data is, to the memory distance between one object initialization and first use
# Input file is supposed already formatted.

# Changed 03/08/2013: for real large files 

from sys import argv
import string, math
import matplotlib.pyplot as plt

script, filename = argv

############### process the origin trace file to get avoid the repeat accesses
#fp = open(filename, 'r')
#f = open('trace-no-repeat', 'w+')
#line_fp = fp.readline()
#temp_info = string.split(line_fp, ' ')
#temp_addr = temp_info[2]

#for templine in fp:
#    info = string.split(templine, ' ')
#    if not info[2] == temp_addr:
#        f.write(info[1])
#        f.write(' ')
#        f.write(info[2])
#        f.write(' ')
#        f.write(info[4])
#    temp_addr = info[2]

#fp.close()
#f.close()
############### process the origin trace file to get avoid the repeat accesses

############### new trace file format is "operation mode, access address, object size"
#tracefile = open('trace-no-repeat', 'r')
tracefile = open(filename, 'r')


object_map = {}           # hashmap used to store all the objects in the trace, it may be huge
target_lnum_map = {}      # hashmap used to store the target object address and line #
target_range_map = {}     # hashmap used to store the target object address and the address range

inter_size_list = []      # list used to store the inter sizes of different targets
target_list = []          # list of the targets for possible future use
inter_addr_list1 = []     # list of the inter addresses in Nursery

line_num = 0              # line number for each object
addr_range = 0
last_addr = '0'           # store the last accessed address

object_size_map = {}      # hashmap used to store all the objects along with the the sizes of each object
addr_list = []            # the list used to record all the objects address, future get the addresses and index
line_num2 = 0
object_size = 0           # the sizes of the objects
inter_arrival_size = 0
i = 0
j = 0
scale = 0                 # for future cache line calculate

# store all the object addresses in one map along with the line number for future index
# store all the object addresses along with the size in the map
# store all the object addresses in the list
for line in tracefile:
    word = string.split(line, ' ')   # word[0] is the operation mode, word[1] is the address
    object_map[word[1]] = line_num

    if (target_lnum_map.has_key(word[1])):
        target_list.append(word[1])
        i = target_lnum_map[word[1]]
        j = line_num
        del target_lnum_map[word[1]]
        for k in range(i, j):                                 # no need to distinguish the boot and heap areas
            m = addr_list[k]
            inter_addr_list1.append(m)
        inter_addr_list1 = list(set(inter_addr_list1))        # remove the duplicate ones
        for x in range(0, len(inter_addr_list1), 1):
            scale = int(object_size_map[inter_addr_list1[x]]/64)        # calculate the cache performance of the memory trace
            inter_arrival_size += (scale+1) * 64
        inter_size_list.append((inter_arrival_size))
    del inter_addr_list1[:]                               # clear the list
    inter_arrival_size = 0                                # make sure every time the inter_arrival_size is zeroed

    if (word[0] == '1') and (not target_lnum_map.has_key(word[1])):
        target_lnum_map[word[1]] = line_num                               # store the address there with the line number
    object_size_map[word[1]] = int(word[2])
    addr_list.append(word[1])

    line_num += 1
## second stage finished

inter_size_sum = 0
for m in range(0, len(inter_size_list), 1):
    inter_size_sum += inter_size_list[m]
average = inter_size_sum/len(inter_size_list)

print "average inter arrival size: ", average
print "maximum inter arrival size: ", max(inter_size_list)

tracefile.close()

x = range(0, len(target_list), 1)
plt.figure(1)
plt.plot(x, inter_size_list, 'k.')
plt.axis([0, len(target_list), 0, max(inter_size_list)])
plt.title('inter_arrival sizes')
plt.xlabel('object addresses list in sequence of accesses')
plt.ylabel('inter arrival sizes in Byte')

plt.savefig(filename + '.png')

# figure 2 is the cumullative measurement figure
plt.figure(2)
inter_size_list.sort();
list_len = len(inter_size_list)
temp = inter_size_list[0]
cnt = 0
inter_size1 = []
perc_list = []
for count in range(0, list_len, 1):
    if inter_size_list[count] == temp:
        cnt += 1
    else:
        percentage = (1.0*cnt/list_len)*100
        inter_size1.append(temp)
        perc_list.append(percentage)
        temp = inter_size_list[count]
inter_size1.append(max(inter_size_list))
perc_list.append(100)

#plt.subplot(211)
plt.plot(inter_size1, perc_list, 'r.')
plt.axis([100, max(inter_size1), 40, 102])
plt.title('Cumulative Distribution Function of inter arrival sizes')
plt.xlabel('inter arrival sizes in Byte')
plt.ylabel('Percentage in %')
plt.savefig('cmf.png')

