#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import sys

def cut_line( line,str1,str2 ):
    #In a one-line text, get the content between two given marks and return it
    #get the mark
    a = line.find(str1)
    b = line.find(str2)
    #return it
    return line[ ( a + len(str1)) : b ] 

def pkts_read( filename,snum ):
    #this function is used to measure one-port-in-one-port-out switch
    #the default switch is 's2'
    file = open(filename,"r")
    receive_sum = [];
    transmit_sum = [];
    while 1:
        line = file.readline()
        if not line:
           break
        #s2-eth1 is the send out port
        if line.find( "s%s-eth1:" % snum) == -1:
           pass
        else:
            #skip to the TX statics line
            line = file.readline()
            line = file.readline()
            #get the total send out bytes static
            totalSend = float( cut_line(line,"packets","bytes") )
            #add the element to the transmitted sum
            transmit_sum.append( totalSend )
        #s2-eth2 is the receive port
        if line.find( "s%s-eth2:" % snum) == -1:
            pass
        else:
            #skip to the RX statics line
            line = file.readline()
            #get the total received bytes static
            totalReceive = float( cut_line(line,"packets","bytes") )
            #add the element to the received sum
            receive_sum.append( totalReceive )
    file.close()
    return (receive_sum,transmit_sum)

def traffic_read(filename):
    file = open(filename,"r")
    meanList = [];
    stdList = [];
    while 1:
        #read line by line
        line = file.readline()
        if not line:
           break
        #Get the mean value
        trafficMean = float( cut_line(line,"trafficMean is","Mbit/s,") )
        meanList.append( trafficMean )
        #Get the std value
        trafficStd = float( cut_line(line,"trafficStd is","Mbit/s\n") )
        stdList.append( trafficStd )
    file.close()
    return (meanList, stdList)

"""This file is used to collect results of each test
   input files are: 's2-eth2TrafficExtract.txt'(the traffic infomation', 'ifconfig.txt'(the loss information)
   output file is: 'autoResult.txt'
   the output format is: trafficMean,trafficStd,bandwid,buff,load,lossRate"""

outFileName = 'autoResult.txt'
ofile = open(outFileName,'w')
outPortBand = [90,] #Mbit/s 37
outPortBuffer = [10, 30, 50, 70, 80, 100, 120, 150]
#outPortBuffer = [1, 3] #ms
(receive_sum, transmit_sum) = pkts_read( filename='ifconfig.txt', snum = '2')
(meanList, stdList) = traffic_read( filename='s2-eth2TrafficExtract.txt')
temp = 0
for bandwid in outPortBand:
    for buff in outPortBuffer:
        for k in range(3): # do 3 times to get the average value
            (trafficMean,trafficStd) = (meanList[temp], stdList[temp])
            ReceivePkt = receive_sum[temp+1] - receive_sum[temp]
            TransminPkt = transmit_sum[temp+1] - transmit_sum[temp]
            load = trafficMean/bandwid
            lossRate=(ReceivePkt-TransminPkt)/ReceivePkt
            temp = temp + 1
            ofile.write("%.5f %.5f %.0f %.5f %.4f %.8f\n"%(trafficMean,trafficStd,bandwid,buff,load,lossRate))
ofile.close()
print "The program runs smoothly"