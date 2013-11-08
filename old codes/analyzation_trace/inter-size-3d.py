# /bin/python
# Junjie Qian
# inter-size-3d.py

# use this to plot 3D figure of the inter sizes of different target objects

from sys import argv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import string


script,filename = argv

tracefile = open(filename, 'r')

inter = []
tmp = []        # this is temporay list to store the inter sizes of one object
#count = 0
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
i = 0

for line in tracefile:
	if line.find('[') == 0:
		del tmp[:]
		count = 0
		count = line.count(',')
		word = string.split(line, ',')
		for n in range(1, count):
			tmp.append(int(word[n]))
		temp = string.split(word[count], ']')
		tmp.append(int(temp[0]))
	#	for item in tmp:
	#		print(item),
	#	print("s\n")
		xs = tmp
		ys = range(0, len(tmp), 1)
		zs = i
#		print i
		ax.bar(ys, xs, zs, zdir='y', color='#eef8ff', alpha=0.8)
		i += 1
# ax.set_xlim(0, 3000)
ax.set_xlabel('Objects')
ax.set_ylabel('Access Sequence')
ax.set_zlabel('Inter sizes of the objects')
plt.axis([0, 3000, 0, 44000])

plt.savefig(filename)

