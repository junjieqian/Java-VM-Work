#!/bin/env/python
# collect-results.py

# collect the benchmark results divided in the address range

from sys import argv
import string, os, math
from os.path import join, getsize

script, dirname, resultname = argv

################ fetech the inter sizes in the sub files
interlist = []
tmplist = []
addrlist = []
for root, dirs, files in os.walk(dirname):
	for f in files:
		print dirname+'/'+f
		fp = open(dirname+'/'+f, 'r')
		for line in fp:
			if line.find('[') == 0:
				tmplist = []
				count = line.count(',')
				if count>0:
					word = string.split(line, ',')
					for n in range(1, count):
						tmplist.append(int(word[n]))
					temp = string.split(word[count], ']')
					tmplist.append(int(temp[0]))
					interlist.append(tmplist)
				else:
					interlist.append([int(0)])
#			elif line.find(':') == 0:
#				pass
			else:
				try:
					word = string.split(line, '\n')
					addrlist.append(int(word[0]))
				except:
					pass

print len(interlist), len(addrlist)

todellist = []
for i in range(0, len(interlist)):
	try:
		if (len(interlist[i]) == 1):
		todellist.append(i)
	except:
		print i, interlist[i]
  
j = 0
for i in todellist:
	del interlist[i-j]
	del addrlist[i-j]
	j += 1
  
print len(interlist), len(addrlist)

print len(interlist), len(addrlist)


####### store the inter sizes to the resultfile
try:
	resultfile = open((resultname+'intersize'), 'w+')
	for item in interlist:
		print >> resultfile, item
#		print item
	resultfile.close()
except:
	print "no result filename provided"

try:
	resultfile2 = open((resultname+'address'), 'w+')
	for item in addrlist:
		print >> resultfile2, item
#		print item
	resultfile2.close()
except:
	print "no result filename provided"

####### calculate the max size, min size and such distribution
num1 = 0
num2 = 0
num3 = 0
num4 = 0
maxsize = 0
minsize = 100
averagesize = 0
meansize = 0
totalsize = 0
cnt = 0
for i in range(0, len(interlist)):
	for j in range(0, len(interlist[i])):
		tmp = interlist[i][j]
		cnt += 1
		totalsize += tmp
		if (maxsize < tmp):
			maxsize = tmp
		elif (minsize > tmp):
			minsize = tmp
		if (tmp < 32768):
			num1 += 1
		elif (tmp < 262144) and (tmp >= 32768):
			num2 += 1
		elif (tmp < 8388608) and (tmp >= 262144):
			num3 += 1
		else:
			num4 += 1

print "32K: ", num1, "  256k: ", num2, "   8M: ", num3, "   larger than 8M:  ", num4

averagesize = totalsize/cnt
tempval = 0                   ########### for (x-mean)^2
for i in range(0, len(interlist)):
    for j in range(0, len(interlist[i])):
        tempval += math.pow((interlist[i][j] - averagesize), 2)
meansize = math.sqrt(tempval/(cnt-1))
print "maxsize: ", maxsize, " minsize: ", minsize, " averagesize: ", averagesize, " meansize: ", meansize

