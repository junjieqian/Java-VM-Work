#!/usr/bin/python

import string
import time
import numpy as np
import matplotlib.pyplot as plt

def printlist(list1, list2, figcnt, figname):
    ''' plot two lists
    '''
    plt.figure(figcnt)
    n=len(list1)
    if n>0:
#        print 'length of the addrlist is: ', n
        p=np.arange(n)
        plt.plot(p, list1, 'bs')
        plt.plot(p, list2, 'g^')
#        plt.axis([0, p])
        plt.title("Access distribution during GC")
        plt.xlabel("GC range")
        plt.ylabel("Object address")

        plt.savefig((figname)+str(int(time.time())))
        figcnt+=1
    return figcnt

def printinfo(inlist, figcnt, bootname):
    plt.figure(figcnt)
    n=len(inlist)
    if n>0:
#        print 'length of the inlist is: ', n
        p=np.arange(n)
        plt.plot(p, inlist, 'k.')
        plt.title("Boot Gen accesses during GC")
        plt.xlabel("GC range")
        plt.ylabel("Object address")

        plt.savefig((bootname)+str(int(time.time())))
        figcnt+=1
    return figcnt

def printratio(inlist, figcnt, rationame):
    plt.figure(figcnt)
    n=len(inlist)
    if n>0:
#        print 'length of the inlist is: ', n
        p=np.arange(n)
        plt.plot(p,inlist,'k.')
        plt.title("Ratio of Nursery:NoNursery accesses during GC")
        plt.xlabel("GC range")
        plt.ylabel("Ratio changes")
        plt.savefig((rationame)+str(int(time.time())))
        figcnt+=1
    return figcnt

def printdistribution(inlist, figcnt, disname):
    plt.figure(figcnt)
    n=len(inlist)
    nums1=[]
    nums2=[]
    nums3=[]
    l1cnt=0
    l2cnt=0
    l3cnt=0
    l4cnt=0
    if n>0:
        for i in range(1, 20):
            l1cnt=0
            l2cnt=0
            l3cnt=0
            l4cnt=0
            lcnt=0
            for j in range(0, n):
                distance=-1
                try:
                    distance=int(inlist[j][i])
                except:
                    continue
                if distance>0:
                    if int(inlist[j][i])<=32768:
                        l1cnt+=1
                    elif int(inlist[j][i])<=262144:
                        l2cnt+=1
                    elif int(inlist[j][i])<=8388608:
                        l3cnt+=1
                    elif int(inlist[j][i])>=8388608:
                        l4cnt+=1
            lcnt=l1cnt+l2cnt+l3cnt+l4cnt
            if lcnt==0:
                break;
            nums1.append(float(float(l1cnt)/float(lcnt)))
            nums2.append(float(float(l1cnt+l2cnt)/float(lcnt)))
            nums3.append(float(float(l1cnt+l2cnt+l3cnt)/float(lcnt)))
#            print l4cnt, ' and ', lcnt, ' and ', i
        ind=np.arange(len(nums3))
        p1=plt.plot(ind, nums1, 'k^')
        p2=plt.plot(ind, nums2, 'bs')
        p3=plt.plot(ind, nums3, 'r-')
        plt.title("Distribution of accesses with different inter sizes in objects' lifetime in Nursery")
        plt.xlabel("Intersize indexes of individual object")
        plt.ylabel("Proportion of different Inter-size between accesses")
        plt.legend((p1[0],p2[0],p3[0]), ('<32kB', '<256kB', '<8MB'), loc='upper center')
#        plt.legend((p3[0]), ('<8m'), loc='upper center')
        plt.savefig((disname) + str(int(time.time())))
        figcnt+=1
    return figcnt
