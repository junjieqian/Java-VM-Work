# !/bin/python
# inter-size.py
# Junjie Qian, jqian@cse.unl.edu

# calculation of the inter arrival size between the initialized objects (first write and then first use).
# 04/16/2013
# all information is stored in the memory to process
# the input file is supposed to have the replicated ones erased, and each line format is "<operation mode> <address> <size>"

from sys import argv
import os, string, math
import matplotlib.pyplot as plt

# first is for the input filename
# second is for the output filename
script, first, second = argv

tracefile = open(first, 'r')

############################## in this example, first store all information in the hashmap and string
sizemap = {}                               # hashmap stores the sizes of all objects
addrlist = []                                     # list of the string for next fetch
rwlist = []
for l in tracefile:
    sequence = string.split(l, ' ')
    sizemap[sequence[1]] = int(sequence[2])
    addrlist.append(sequence[1])
    rwlist.append(sequence[0])

tracefile.close()
###############################################################################

target_map = {}          # hash map used to store the target objects, initialized objects, write and then first use
target_list = []         # list used to store the target objects in the order of its inter sizes stored

######## inter_size_list.append(target_inter_size_list) ###### the objects are in same order as the target list
inter_size_list = []          # all the inter sizes stored in this list

inter_list = []          # store the inter objects between the target objects

rw = 0                  # read write operation mode of the target objects
addr = ''                # address of the target objects
size = 0                 # size of the target objects

begin = 0                # begin index of the inter arrival objects list
end = 0                  # end index of the inter arrival objects list

line = 0                 # line number of each object
limit = len(addrlist)
for n in range(0, limit):
    addr = addrlist[n]
    rw = int(rwlist[n])
    line = n
    if (target_map.has_key(addr)):
        begin = target_map[addr]
        end = line

        # update the line number of target in the hashmap
        target_map[addr] = line

        # find whether this object is in the inter size list, if not add it into the target list
        if not (addr in target_list):
            target_list.append(addr)
            # this is for sure there would be same index or elements in both list, and future calculation should eliminate one occurrance
            inter_size_list.append([0])           

        for i in range(begin, end):
            inter_list.append(addrlist[i])
        inter_list = list(set(inter_list))        # remove the duplicate ones	

        # there are several versions of the memory size calculation, 
        # one is get the cache performance, which put the objects together unless the sum of the size is over 64 (cache line size)
        # another one is get the memory size, which is plus all the object sizes togeter
        # one more is to get all the changes of the objects' inter sizes
        tmp = 0
        inter_size = 0                           # the total inter_size of the target objects
        ######################## first one type, for 64B cache line
        for i in range(0, len(inter_list)):
            if (tmp + sizemap[inter_list[i]]) < 64:
                tmp += sizemap[inter_list[i]]
            elif (tmp + sizemap[inter_list[i]]) == 64:
                tmp = 0
                inter_size += 64
            elif ((tmp + sizemap[inter_list[i]]) > 64) and ((sizemap[inter_list[i]]) < 64):
                tmp = sizemap[inter_list[i]]
                inter_size += 64
            elif ((tmp + sizemap[inter_list[i]]) > 64) and ((sizemap[inter_list[i]]) >= 64):
                tmp = sizemap[inter_list[i]] % 64
                inter_size += 64 * int((sizemap[inter_list[i]])/64)
        ####################### second one type, all memory sizes
##        for i in range (0, len(inter_list)):
##            inter_size += object_size_map[inter_list[i]]

        target_index = target_list.index(addr)                  # get the index of this target in the target list
        inter_size_list[target_index].append(inter_size)

    # store the target address to the map, if it is not in the map
    if (rw == 1) and (not target_map.has_key(addr)):
        target_map[addr] = line

    del inter_list[:]

#########################calculate out different inter sizes' proportions, 32K, 256K, 8M######
num1 = 0
num2 = 0
num3 = 0
num4 = 0
for i in range(0, len(inter_size_list)):
    for j in range(0, len(inter_size_list[i])):
        if inter_size_list[i][j] < 32768:
            num1 += 1
        elif inter_size_list[i][j] < 262144:
            num2 += 1
        elif inter_size_list[i][j] < 8388608:
            num3 += 1
        else:
            num4 += 1

num1 -= len(inter_size_list)           # refer to previous inter_size_list add one more 0 accurance

print "32K: ", num1, "  256k: ", num2, "   8M: ", num3, "   larger than 8M:  ", num4

#########################calculate out different inter sizes' maximum, minimize, mean, std. mean
sumval = 0
minval = 0
maxval = 0
meanval = 0
stdval = 0
count = 0
for i in range(0, len(inter_size_list)):
    for j in range(0, len(inter_size_list[i])):
        count += 1
        sumval += inter_size_list[i][j]
        if minval > inter_size_list[i][j]:
            minval = inter_size_list[i][j]
        elif maxval < inter_size_list[i][j]:
            maxval = inter_size_list[i][j]
meanval = sumval/count
tempval = 0                   ########### for (x-mean)^2
for i in range(0, len(inter_size_list)):
    for j in range(0, len(inter_size_list[i])):
        tempval += math.pow((inter_size_list[i][j] - meanval), 2)
stdval = math.sqrt(tempval/(count-1))
print "minimum val: ", minval, "        maximum val:  ", maxval, "      mean val: ", meanval, "   std mean val: ",   stdval

####################### print out the 3D graph
resultfile = open(second, 'w+')
resultfile.write('target_list: \n')
for item1 in target_list:
    print >> resultfile, item1
result_file.write('inter size list: \n')
for item2 in inter_size_list:
    print >> resultfile, item2
resultfile.close()