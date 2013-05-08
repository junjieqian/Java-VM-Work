# !/bin/env/python
# objectnum-timperiod.py

# measure the number of objects with big inter arrival sizes in different period of execution life time.

import string, sys
from sys import argv
import matplotlib.pyplot as plt

#script, intersizefile, addressfile, tracefile, resultname = argv

try:
  script, intersizefile, addressfile, tracefile, resultname = argv
except:
  sys.exit('usage, python objectnum-timeperiod.py "inter size file name" "inter size address file name" "original trace file name" "result PNG file name"')

interlist = []
tmplist = []
fp = open(intersizefile, 'r')
for line in fp:
  if line.find('[') == 0:
    tmplist = []
    count = line.count(',')
    if count>0:
      word = string.split(line, ',')
      tmplist.append(int((string.split(word[0], '['))[1]))
      for n in range(1, count):
        tmplist.append(int(word[n]))
      temp = string.split(word[count], ']')
      tmplist.append(int(temp[0]))
      interlist.append(tmplist)
    else:
      word = string.split(line, ']')
      tmplist.append(int((string.split(word[0], '['))[1]))
      interlist.append(tmplist)

fp.close()

fa = open(addressfile, 'r')
bigaddrlist = []
for line2 in fa:
  word = string.split(line2, '\n')
  bigaddrlist.append(word[0])
fa.close()

m = len(interlist)
if m != len(bigaddrlist):
  print 'Attention!!, check the inter size code, that two length doesnot equal: ',m, len(bigaddrlist)

badaddrlist = []
badaddrindexlist = []
for i in range(0, 200):
  for j in range(0, m):
    try:
      size = interlist[j][i]
      if (int(size)>=8388608):
        badaddrindex = -1
        badaddrtmp = 0
        try:
          while 1:
            try:
              badaddrindex = badaddrlist.index(bigaddrlist[j], badaddrindex+1)
            except:
              badaddrindex = -1
            if badaddrindex>=0:
              badaddrtmp = int(badaddrindexlist[badaddrindex])
            else:
              badaddrtmp = 0
        except:
          pass
        badaddrindexlist.append(i-badaddrtmp)
        badaddrlist.append(bigaddrlist[j])
    except:
      pass

del bigaddrlist[:]
del interlist[:]

fc = open(tracefile, 'r')
i = 0
timelist = []
acceslist = []
addrindex = -1
for line3 in fc:
  word = string.split(line3, ' ')
  addr = word[1]
  if addr in badaddrlist:
    addrindex = badaddrlist.index(addr)
    if int(badaddrindexlist[addrindex]) > 1:
      badaddrindexlist[addrindex] = int(badaddrindexlist[addrindex]) - 1
      accesslist.append(0)
    else:
      accesslist.append(1)
      del badaddrlist[addrindex]
      del badaddrindexlist[addrindex]
  else:
    accesslist.append(0)
  timelist.append(i)
  i += 1

fc.close()

timelength = len(timelist)
if timelength != len(accesslist):
  sys.exit('Error happens here, lenght of time list doesnot equal to acces list!')

i = 0
newtimelist = []
newaccesslist = []
periodaccess = 0
periodtime = 0
for i in range(0, timelength):
  if i%1000 == 0:
    newtimelist.append(i)
    newaccesslist.append(periodaccess)
    periodaccess = 0
    periodtime = 0
  else:
    periodaccess += 1
    periodtime += 1
newaccesslist.append(periodaccess)
newtimelist.append(i)

ind = np.arange(len(newaccesslist))
p1 = plt.bar(ind, newaccesslist)
plt.ylabel('total object number with inter arrival sizes larger than 8M')
plt.xlabel('every 1000 accesses during the execution lifetime')
plt.tite('number change of objects with inter arrival size larger than 8M during the execution, %s'%(resultname))
plt.savefig(resultname)





