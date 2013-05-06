# !/bin/env/python
# boxplotting-intersize.py
# Junjie Qian, May 1st, 2013

# to plot the box of inter size arrange. The Xlabel is the index of inter sizes, ylabl is the inter sizechange

import os, string, math
from sys import argv
import matplotlib.pyplot as plt
import numpy as np

script, sourcename, resultname = argv

interlist = []
tmplist = []
fp = open(sourcename, 'r')
for line in fp:
  if line.find('[') == 0:
    tmplist = []
    count = line.count(',')
    if count > 0:
      word = string.split(line, ',')
      tmplist.append(int((string.split(word[0], '['))[1]))
      for n in range(1, count):
        tmplist.append(int(word[n]))
      temp = string.split(word[count], ']')
      tmplist.append(int(temp[0]))
      interlist.append(tmplist)

fp.close()
m = len(interlist)
x = []   # range of inter list at each access
# be care if no intersize for one access, that would not be count
# e.g. [1,2] and [1,2,3], the third one would be only one
tmpx = []   # to store the nth element of each inter size list
size = 0

for i in range(0, 200):
  tmpx = []
  x.append([])
  for j in range(0, m):
    try:
      size = interlist[j][i]
      tmpx.append(size)
    except:
      pass
  x[i] += tmpx


interlist = []     # empty the interlist
# x[] is the list of the nth accesses
nums1 = []
nums2 = []
nums3 = []
nums4 = []
numstotal = []
numsmean = []
size1 = 0
size2 = 0
size3 = 0
size4 = 0
totoalsize = 0
meansize = 0
for i in range (0, len(x)):
  size1 = 0
  size2 = 0
  size3 = 0
  size4 = 0
  totalsize = 0
  total = 0
  meansize = 0
#  print i, len(x[i])
#  print x[i]
  if (len(x[i])>0):
    for j in range (0, len(x[i])):
      totalsize += x[i][j]
      total += 1
      if (x[i][j]<32768):
        size1 += 1
      elif (x[i][j]>=32768) and (x[i][j]<262144):
        size2 += 1
      elif (x[i][j]>=262144) and (x[i][j]<8388608):
        size3 += 1
      else:
        size4 += 1
#    print total, size1, size3, float(float(size2)/float(total)), float(size3/total), float(size4/total)
    nums1.append(float(float(size1)/float(total)))
    nums2.append(float(float(size2)/float(total)))
    nums3.append(float(float(size3)/float(total)))
    nums4.append(float(float(size4)/float(total)))
    numstotal.append(totalsize)
    numsmean.append(float(totalsize/len(x[i])))

ind = np.arange(len(nums1))

#print nums1
#print nums2
#print nums3
#print nums4

a = []
b = []
for i1, i2, i3 in zip(nums1, nums2, nums3):
  a.append(i1+i2)
  b.append(i1+i2+i3)

p1 = plt.bar(ind, nums1, color = 'r')
p2 = plt.bar(ind, nums2, bottom= nums1, color = 'g')
p3 = plt.bar(ind, nums3, bottom= a, color = 'y')
p4 = plt.bar(ind, nums4, bottom= b, color = 'b')

plt.ylabel('distributions of different intersizes')
plt.xlabel('indexes of accesses')
plt.title('inter sizes distributions of different accesses')
#plt.xticks(ind, np.arange(0,1000,100))
#plt.legend(loc = 'upper center', ncol =3, fancybox = True, shadow=True, (p1[0], p2[0], p3[0], p4[0]), ('<32k', '32k-256k', '256k-8m', '>8m'))
plt.legend((p1[0], p2[0], p3[0], p4[0]), ('<32k', '32k-256k', '256k-8m', '>8m'), loc = 'upper center', ncol =4, fancybox = True, shadow=True)
plt.savefig(resultname)


#plt.boxplot(x,0,'')
#plt.xlabel('index of access')
#plt.ylabel('inter size')
#plt.title('inter sizes of different accesses')

#plt.savefig(resultname)

#resultfile = open(resultname, 'w+')
#for element in x:
#  print >>resultfile, element
#resultfile.close()
