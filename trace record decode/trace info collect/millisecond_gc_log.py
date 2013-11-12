#!/usr/bin/python
# millisecond_gc_log.py
# this python function analyze the trace records time stamped with seconds
# the time stamps are real system time, so needs to take differentiate time

import string
import sys
import math
#sys.path.append(os.path.join(os.path.dirname(__file__), 'pyro'))
from pyro import gc_plot
from pyro import gc_info_read
from pyro import instruction_translate

class g:
    # global figname
    # global bootname
    # global rationame
    # global disname
    # global cnt
    # global figcnt
    figname='gc_plot_'
    bootname='boot_plot_'
    rationame='ratio_plot_'
    disname='dis_plot_'
    cnt=0
    figcnt=0

def millisecond_gc_log(filename, gclog, cachefile, fullcachein):
    ''' second_gc_log function
    Memory trace processing, memory trace is timestamped with seconds
    @param fp, trace file name
    @param fw, cache simulation input file name, file trace without BIAS access (mostly first access of BIAS objects')
    @param fa, cache simulation input file name, full trace records (for comparison)
    @param biaslist, list to save the BIAS accesses

    @param l1cnt, count the accesses larger than 32kB
    @param l2cnt, count the accesses larger than 256kB
    @param l3cnt, count the accesses larger than 8MB

    @param time_list, store the gc happen time in log file
    @param nursery_down/heap_up/heap_down, store the heap address range in log file
    '''
    fp = open(filename, 'r')
    fw = open(cachefile, 'w')
    fa = open(fullcachein, 'w')
    time_list = []
    time_list = gc_info_read.gc_read(gclog)
    for i in range(len(time_list)):
        time_list[i] = int(1000*float(time_list[i]))
    (nursery_down, heap_up, heap_down) = gc_info_read.range_read(gclog)
    biaslist = []         # save the BIAS accesses
    biasdict = {}         # save the BIAS objects
    l1list = []           # save the accesses larger than 32kB 
    l2list = []           # save the accesses larger than 256kB
    l1cnt = 0
    l2cnt = 0
    l3cnt = 0
    nurserylist = []      # record the nursery access
    nonurserylist = []
    ratiolist = []
    bootlist = []
    intersizelist = []    # record the inter size list of each object
    inst_list = []        # record the instruction usage
    objdict = {}          # record the index of object in intersizelist to save finding time
    sizedict = {}         # record the newest max size of object last accesses
    boot = 0              # record the access # of the boot area objects
    nursery = 0           # record the access # of the nursery objects
    nonursery = 0         # record the access # of the non-nursery objects
    count = 0
    maxaddr = 0           # suppose the current highest address in nursery generation of heap

    for line in fp:
        addr=0
        time_stamp=0

        if line.find(',')>0:
            try:
                word = line.split(',')
                addr = int(word[0], 0)
                inst = word[1].split('\n')[0]
            except:
                pass
        else:
            try:
                time_stamp = int(line.split('\n')[0], 0)
            except:
                pass

#        if line.find('GC')>=0:
        # for the second condition, because some trace records are messed, so limited it to reasonable range (12/31/2014)
        if (str(time_stamp) in time_list) or (time_stamp>=int(time_list[0]) and time_stamp<int('1419984000')): 
            del time_list[0]
            time_list.append(str(int('0xffffffff', 0)))
#            g.figcnt = gc_plot.printlist(nurserylist, nonurserylist, g.figcnt, g.figname)
#            g.figcnt = gc_plot.printinfo(bootlist, g.figcnt, g.bootname)
#            g.figcnt = gc_plot.printratio(ratiolist, g.figcnt, g.rationame)
#            g.figcnt = gc_plot.printdistribution(intersizelist, g.figcnt, g.disname)
            print "BIAS list access number is: ", l3cnt #len(biaslist)
#            print "BIAS list object number is: ", len(biasdict)
            print "Inter size larger than L1 32KB, access number is: ", l1cnt #len(l1list)
#            print "Inter size larger than L1 32KB, object number is: ", len(list(set(l1list)))
            print "Inter size larger than L2 256KB, access number is: ", l2cnt #len(l2list)
#            print "Inter size larger than L2 256KB, object number is: ", len(list(set(l2list)))
            print "Total object number is: ", len(objdict)
            print "Nursery accesses is: ", nursery
            print "Nonursery accesses is: ", nonursery
            nursery=0
            boot=0
            count=0
            nonursery=0
            del nurserylist[:]
            del bootlist[:]
            del nonurserylist[:]
            del ratiolist[:]
            del intersizelist[:]
            del biaslist[:]
            del l1list[:]
            del l2list[:]
            biasdict.clear()
            objdict.clear()
            sizedict.clear()
            g.cnt+=1
            maxaddr=0
            print 'GC happens @ ', line
            continue

        if addr>0:
            if addr>int('0x11111111', 0) and addr<int('0xffffffff', 0):
                fa.write('1 ')
                fa.write(str(hex(addr)))
                fa.write('\n')
            if addr<=int(heap_up, 0) and addr>=int(heap_down, 0):
                if addr>=int(nursery_down, 0):
                    nursery+=1
                    count+=1
                    if addr>maxaddr:
                        maxaddr=addr
                    if addr in objdict:
                        distance=abs(sizedict[addr]-maxaddr)
                        if distance>=8388608:
                            l3cnt +=1
#                            biaslist.append(addr)
#                            inst_list.append(instruction_translate.inst_trans(inst))
#                            print 'inst'
                            if addr in biasdict:
                                biasdict[addr]+=1
                            else:
                                biasdict[addr]=0
                        else:
                            fw.write('1 ')
                            fw.write(str(hex(addr)))
                            fw.write('\n')
                            if distance>=262144:
#                                l2list.append(addr)
                                l2cnt += 1
                            elif distance>=32768:
                                l1cnt += 1
#                                l1list.append(addr)
                        index=objdict[addr]
                        intersizelist[index].append(distance)
                        sizedict[addr]=maxaddr
                    else:
                        fw.write('1 ')
                        fw.write(str(hex(addr)))
                        fw.write('\n')
                        sizedict[addr]=addr
                        objdict[addr]=len(intersizelist)
                        intersizelist.append([0])
                else:
                    count+=1
                    nonursery+=1

#    g.figcnt = printlist(nurserylist, nonurserylist, g.figcnt, g.figname)
#    g.figcnt = gc_plot.printratio(ratiolist, g.figcnt, g.rationame)
#    g.figcnt = gc_plot.printdistribution(intersizelist, g.figcnt, g.disname)
    fp.close()
    print "BIAS list access number is: ", len(biaslist)
    print "BIAS list object number is: ", len(biasdict)
    print "Inter size larger than L1 32KB, access number is: ", len(l1list)
    print "Inter size larger than L1 32KB, object number is: ", len(list(set(l1list)))
    print "Inter size larger than L2 256KB, access number is: ", len(l2list)
    print "Inter size larger than L2 256KB, object number is: ", len(list(set(l2list)))
    print "Total object number is: ", len(objdict)
    print "nursery accesses is: ", nursery
    print "nonursery accesses is: ", nonursery

'''
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print 'Instruction of BIAS accesses list: \n'
    inst_list=list(set(inst_list))
    for element in inst_list:
        print element
'''
