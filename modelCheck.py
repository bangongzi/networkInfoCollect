#!/usr/bin/python
# -*- coding: utf-8 -*-

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
    #get the average rate, unit is Gbit/s
    rate = (sum0/count)/1000000000
    load = rate/bandwidth   
    print "The average speed is %.4fGbit/s,the bandwidth is %.4fGbit/s,the load of s2 is %.4f" %( rate,bandwidth,load )
    file.close()
    return 


def readtxt(str,send_pkt,retrans_pkt,depth = 1 ):
    filename = str + "netstat.txt"
    file = open(filename,"r")
    trans_sum = [];
    retrans_sum = [];
    while 1:
        line = file.readline()
        if not line:
            break
        if line.find("segments send out") == -1:
            pass
        else:
            i=line.find("segments send out")-1
            str = line[4:i]
            trans_sum.append(int(str))
        if line.find("segments retransmited") == -1:
            pass
        else:
            i=line.find("segments retransmited")-1
            str = line[4:i]
            retrans_sum.append(int(str))
    j = len(trans_sum)-depth
    SendPkt = trans_sum[j] - trans_sum[j-1]
    j = len(retrans_sum)-depth
    RetransPkt = retrans_sum[j] - retrans_sum[j-1]
    send_pkt.append(SendPkt)
    retrans_pkt.append(RetransPkt)
    file.close()
    return

def loss_rate_get(left,right):
    txt_read_num = right -left + 1
    send_pkt = []
    retrans_pkt = []
    #The first element is used to store the total
    #number of packets retransmitted,the second for 
    #packets send,the third is for packet lost rate
    rate = [0,0,0]
    for i in xrange(left,right+1):
        string ='/home/bird/log/netstat/sr' + str(i)
        readtxt(str=string,send_pkt = send_pkt,retrans_pkt = retrans_pkt)
    for i in xrange(0,txt_read_num):
        rate[0] += retrans_pkt[i]
        rate[1] += send_pkt[i]
    rate[2] = rate[0]/rate[1]
    print "Here are numbers of retrans/send packets of h%s to h%s:" %(str(left),str(right))
    print retrans_pkt,"\n",send_pkt
    print "The total packet loss rate is:%.8f" %rate[2]

if len(sys.argv) == 3:
    fname = 'ifconfig.txt'
    #load_get( bandwidth=float(sys.argv[1]),test_time=float(sys.argv[2]),snum='2',filename=fname )
    print "The latency of s2-eth1 is %s" %sys.argv[2]
    loss_rate_get( left=1,right=200 )
    #process the traffic
    os.system("python traffic_process.py")
    #get the average speed,get the average load, then print it
    load_get( bandwidth=float(sys.argv[1]),filename='s2-eth2_traffic.txt')
else:
    print "Invalid number of parameters.\nThe right form is ./switch_process.py 10(Gbit/s switch bandwidth) 1ms(latency mark)"
