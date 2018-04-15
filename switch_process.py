#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Usage: $ python switch_process.py 30(Mbit/s) 20ms
    The first para is the port bandwidth, the second is the buffer size
    This file will return the load factor and the packets loss rate of 
    one given port in the last traffic period"""

from __future__ import division
import sys
import os
import time

def cut_line( line,str1,str2 ):
    #In a one-line text, get the content between two given marks and return it
    #get the mark
    a = line.find(str1)
    b = line.find(str2)
    #return it
    return line[ ( a + len(str1)) : b ] 


def low_load_get( bandwidth,test_time,snum,filename='ifconfig.txt' ):
    """Calculate the load factor of the two statics
       rated bandwidth,test time is needed"""
    file = open(filename,"r")
    traffic = []
    while 1:
        line = file.readline()
        if not line:
            break
        if line.find('s'+snum+'-eth1:') == -1:
            pass
        else:
            #skip two lines to the TX line
            line = file.readline()
            line = file.readline()
            #get the transmitted bytes
            totalBytes = float( cut_line( line=line,str1="bytes",str2="(") )
            #Add to the traffic list
            traffic.append( totalBytes )
    #Get the newest transmitted data,transfer to GBytes
    data = (traffic[-1]-traffic[-2])/1000000000
    #Calculate rate(Gbit/s)
    rate = (data*8)/test_time
    #Calculate load
    load = rate/bandwidth
    file.close()
    print "The average speed is %.4fGbit/s,the bandwidth is %.4fGbit/s,the load of s%s is %.4f" %( rate,bandwidth,snum,load )

def load_get( bandwidth, filename ):
    file = open(filename,"r")
    sum0,count = ( 0, 0 ) 
    while 1:
        line = file.readline()
        if not line:
            break
        #get the traffic, unit is bit/s
        sum0 += float( cut_line( line, " ", "\0" ) )
        count += 1
    #get the average rate, unit is Mbit/s
    rate = (sum0/count)/1000000
    load = rate/bandwidth   
    print "The average speed is %.4fMbit/s,the bandwidth is %.4fMbit/s,the load of s2 is %.4f" %( rate,bandwidth,load )
    file.close()
    return 

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
    #Get the single result by substraction
    ReceivePkt = receive_sum[-1] - receive_sum[-2]
    TransminPkt = transmit_sum[-1] - transmit_sum[-2]
    file.close()
    return (ReceivePkt,TransminPkt)

def loss_rate_get( snum='2',filename='ifconfig.txt' ):
    #Calculate the packets lost rate between two statics 
    ReceivePkt,TransminPkt = pkts_read( filename,snum )
    rate = (ReceivePkt - TransminPkt) / ReceivePkt
    print "switch s%s receive %d pkts,send %d pkts,so loss rate is: %.7f" % (snum,ReceivePkt,TransminPkt,rate)


if len(sys.argv) == 3:
    fname = 'ifconfig.txt'
    #load_get( bandwidth=float(sys.argv[1]),test_time=float(sys.argv[2]),snum='2',filename=fname )
    print "The latency of s2-eth1 is %s" %sys.argv[2]
    loss_rate_get( snum = '2',filename=fname )
    #process the traffic
    os.system("python traffic_process.py")
    #get the average speed,get the average load, then print it
    load_get( bandwidth=float(sys.argv[1]),filename='s2-eth2_traffic.txt')
else:
    print "Invalid number of parameters.\nThe right form is ./switch_process.py 10(Mbit/s switch bandwidth) 1ms(latency mark)"
