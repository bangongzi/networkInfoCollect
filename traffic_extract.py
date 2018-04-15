#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Usage: $ python traffic_extract.py
    This file is used to calculate the mean value and the standard deviation of the traffic
   input file is 'traffic_rough.txt', output file is 's2-eth2TrafficExtract.txt'
   Each call of this file will only add one line to the output file"""

from __future__ import division
import sys

def line_process(line):
    p1=line.find('t:')
    p2=line.find('s:')
    if p1 < 0 or p2 < 0:
        print "File formation is not right\n"
        print "Make sure lines in the file like: Moment:12.234   Bytes:2345"
        return
    momenter=float(line[(p1+2):(p2-5)])
    byter=int(line[(p2+2):])
    return (momenter,byter)

snum="2"
sfname="traffic_rough.txt"
tfname="traffic_transition.txt"
ofname="s%s-eth2TrafficExtract.txt"%snum

#part1 Get timestamp and traffic sum of every moment
sfile = open(sfname,"r")
tfile = open(tfname,"w")
#the unit of traffic_sum is "byte"
time = traffic_sum = count = 0
while 1:
    line = sfile.readline()
    #stop when the file is finished
    if not line:
        break
    #find the start mark "NewStart"
    if line.find('NewStart') == -1:
        pass
    #update timestamp and clear traffic_sum
    else:
        #put timestamp and traffic_sum of last mark into transition.txt
        #skip the very start where time is '0'
        if time > 0:
            tfile.write("Moment:%.5f   Bytes:%d\n"%(time,traffic_sum) )
        #update the timestamp
        p1=line.find('art')
        time =float(line[(p1+4):])
        #clear the traffic_sum
        traffic_sum = 0
    #find the given switch like "s301"
    if line.find('s'+snum+'-eth') == -1:
        pass
    else:
        #skip port 1, cause it is the add-up port 
        if line.find('s'+snum+'-eth1:') == -1:
            #skip two lines to the "RX" statics line
            line = sfile.readline()
            #get the "bytes" static
            a = line.find("bytes")
            b = line.find("(")
            #add other port statics
            traffic_sum += int(line[a+5:b])           
        else:
            continue           
sfile.close()
tfile.close()

#part2
sfile = open(tfname,"r")
ofile = open(ofname,"a")
#read the first row of transition.txt
line=sfile.readline()
m1=b1=0
m2,b2=line_process(line) #m means moment , b means how many bytes are sent or received from the first place
#make the moment start with zero
base = int(m2)
m2 = m2 - base
trafficList = [] #record every traffic
trafficSum = 0 #total traffic of every periods
recordNum = 0 #how many traffic records
temp = 0
while 1:
    line = sfile.readline()
    #make sure 
    if not line:
        break
    ( m1, b1 ) = ( m2, b2 )
    m2,b2 = line_process(line)
    m2 = m2 - base
    temp = ((b2-b1)*8) / (m2-m1) #get the ture traffic(bit/s)
    trafficList.append(temp)
    trafficSum = trafficSum + temp
    recordNum += 1
trafficMean = trafficSum/recordNum 
temp = 0
for b2 in trafficList:
    temp = temp + (b2 - trafficMean)**2
trafficStd = (temp/recordNum)**(0.5)
ofile.write("trafficMean is %.5fMbit/s, trafficStd is %.5fMbit/s\n"%( trafficMean/1000000, trafficStd/1000000))  
sfile.close()
ofile.close()