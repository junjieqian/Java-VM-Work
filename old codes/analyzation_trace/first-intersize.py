# !/bin/env/python
# first-inter-size.py
# Junjie Qian, jqian@cse.unl.edu

# read through the file, only analyze the first inter arrival size
# this is only temporary result analysis

import string
from sys import argv
import matplotlib.pyplot as plt

script, sourcename, resultname = argv

sourcefile = open(sourcename, 'r')

targetlist = []
targetmap = {}
intersizelist = []
addrlist = []
sizemap = {}
linenum = 0

for line in sourcefile:
	interlist = []
	intersize = 0
	index = 0
	word = string.split(line, ' ')
	rw = int(word[0])
	address = word[1]
	size = int(word[2])
	addrlist.append(address)
	sizemap[address] = size

	if targetmap.has_key(address):
		if not targetmap[address] == 1:
			begin = targetmap[address]
			end = linenum
			targetmap[address] = 1
			for i in range(begin, end):
				interlist.append(addrlist[i])
			interlist = list(set(interlist))
			for item in interlist:
				intersize += sizemap[item]
			targetlist.append(address)
			intersizelist.append(intersize)

	if (rw == 1) and (not targetmap.has_key(address)):
		targetmap[address] = linenum
#		targetlist.append(address)

	linenum += 1

sourcefile.close()
#########################calculate out different inter sizes' proportions, 32K, 256K, 8M######
num1 = 0
num2 = 0
num3 = 0
num4 = 0
for i in range(0, len(intersizelist)):
	if intersizelist[i] < 32768:
		num1 += 1
	elif intersizelist[i] < 262144:
		num2 += 1
	elif intersizelist[i] < 8388608:
		num3 += 1
	else:
		num4 += 1

print "32K: ", num1, "  256k: ", num2, "   8M: ", num3, "   larger than 8M:  ", num4

######################### plot this figure
plt.figure(1)
x = range(0, len(targetlist), 1)
plt.plot(x, intersizelist, 'k.')
plt.axis([0, len(targetlist), 0, max(intersizelist)])
plt.title('first inter_arrival size of objects')
plt.xlabel('object addresses list in sequence of accesses')
plt.ylabel('inter arrival sizes in Byte')

plt.savefig(resultname)