#!/usr/bin/env python3
# coding: utf-8

import argparse
from collections import defaultdict
import re

dict_base = defaultdict(list)
# p2020_18491 tcp_64 141 142 141 142 141
dict_base['p2020_18491'].append(139)
# p2020_18491 tcp_1024 921 912 915 928 932
dict_base['p2020_18491'].append(900)
# p2020_18491 tcp_65536 940 940 940 940 940
dict_base['p2020_18491'].append(940)
# p2020_18491 udp_1400 617 615 614 617 627
dict_base['p2020_18491'].append(515)
# zynq7k_28385 tcp_64 90 87.6
dict_base['zynq7k_28385'].append(93.1)
# zynq7k_28385 tcp_1024 370
dict_base['zynq7k_28385'].append(383)
# zynq7k_28385 tcp_65536 608
dict_base['zynq7k_28385'].append(503)
# zynq7k_28385 udp_1400 954
dict_base['zynq7k_28385'].append(954)
# p4080_18994 tcp_64
dict_base['p4080_18994'].append(195)
# p4080_18994 tcp_1024 
dict_base['p4080_18994'].append(938)
# p4080_18994 tcp_65536
dict_base['p4080_18994'].append(938)
# p4080_18994 udp_1400
dict_base['p4080_18994'].append(893)
# p4080_18995 tcp_64 140 139 140 139 139
dict_base['p4080_18995'].append(147)
# p4080_18995 tcp_1024 912 910 908 915 909
dict_base['p4080_18995'].append(929)
# p4080_18995 tcp_65536 940 940 911 940 939
dict_base['p4080_18995'].append(939)
# p4080_18995 udp_1400 955 954 955 955 954
dict_base['p4080_18995'].append(954)
# am335x_22599 tcp_64 47.9 57.3 50.6 41.9 51.2
dict_base['am335x_22599'].append(48.1)
# am335x_22599 tcp_1024 157 158 156 158 158
dict_base['am335x_22599'].append(141)
# am335x_22599 tcp_65536 414 414 411 417 417
dict_base['am335x_22599'].append(399)
# am335x_22599 udp_1400 225 225 225 227 227
dict_base['am335x_22599'].append(215)
# imx6_25005 tcp_64 106 106 106 107 107
dict_base['imx6_25005'].append(106)
# imx6_25005 tcp_1024 345 346 346 350 349
dict_base['imx6_25005'].append(348)
# imx6_25005 tcp_65536 409 410 413 423 426
dict_base['imx6_25005'].append(427)
# imx6_25005 udp_1400 460 460 460 460 460
dict_base['imx6_25005'].append(460)
# idpQ35_18180 tcp_64 413 415 411 415
dict_base['idpQ35_18180'].append(263)
# idpQ35_18180 tcp_1024 902 940 874 869
dict_base['idpQ35_18180'].append(940)
# idpQ35_18180 tcp_65536 940 888 940
dict_base['idpQ35_18180'].append(940)
# idpQ35_18180 udp_1400 955 955 955 955
dict_base['idpQ35_18180'].append(955)
# t2080_22041 tcp_64 
dict_base['t2080_22041'].append(161)
# t2080_22041 tcp_1024 
dict_base['t2080_22041'].append(940)
# t2080_22041 tcp_65536 
dict_base['t2080_22041'].append(940)
# t2080_22041 udp_1400 
dict_base['t2080_22041'].append(955)
# k2e_28384 tcp_64 
dict_base['k2e_28384'].append(70.2)
# k2e_28384 tcp_1024 
dict_base['k2e_28384'].append(511)
# k2e_28384 tcp_65536 
dict_base['k2e_28384'].append(689)
# k2e_28384 udp_1400 
dict_base['k2e_28384'].append(822)
# idpQ35_18202 tcp_64 
dict_base['idpQ35_18202'].append(404)
# idpQ35_18202 tcp_1024 
dict_base['idpQ35_18202'].append(731)
# idpQ35_18202 tcp_65536 
dict_base['idpQ35_18202'].append(940)
# idpQ35_18202 udp_1400 
dict_base['idpQ35_18202'].append(955)
# zcu102_25087_tcp_64 
dict_base['zcu102_25087'].append(195)
# zcu102_25087_tcp_1024 
dict_base['zcu102_25087'].append(940)
# zcu102_25087_tcp_65536 
dict_base['zcu102_25087'].append(940)
# zcu102_25087_tcp_65536 
dict_base['zcu102_25087'].append(955)
# am437x_28381 tcp_64
dict_base['am437x_28381'].append(97.9)
# am437x_28381 tcp_1024
dict_base['am437x_28381'].append(239)
# am437x_28381 tcp_65536
dict_base['am437x_28381'].append(437)
# am437x_28381 udp_1400
dict_base['am437x_28381'].append(348)
# ls102a_28380 tcp_64
dict_base['ls102a_28380'].append(404)
# ls102a_28380 tcp_1024
dict_base['ls102a_28380'].append(731)
# ls102a_28380 tcp_65536
dict_base['ls102a_28380'].append(940)
# ls102a_28380 udp_1400
dict_base['ls102a_28380'].append(955)

def get_throughput(log):
    """
    """

    dict_data = {}
    with open(log,'r') as f:
        pat = re.compile(r'iperf3.*-l\s(\d+)')
        for line in f:
            line = line.strip()
            m = pat.search(line)
            if m:
                dict_data.setdefault('frame',m.group(1))
            if line.endswith('sender'):
                data = line.split()[-3]     
                dict_data.setdefault('sender',data)
            if line.endswith('receiver'):
                data = line.split()[-3]
                dict_data.setdefault('receiver',data)
            if line.endswith('%)'):
                data = line.split()[-6]
                dict_data.setdefault('sender',data)
    return dict_data

if __name__ == '__main__':

    parse = argparse.ArgumentParser()
    parse.add_argument('-f', '--file', help='log file to process', dest='filename', required=True)
    parse.add_argument('-n', '--num', help='case to execute', dest='casenum', required=True)
    parse.add_argument('-b', '--board', help='the board name', dest='board', required=True)
    args = parse.parse_args()
  
    log = args.filename
    num = args.casenum
    board = args.board
    dict_data = get_throughput(log)

    if float(dict_data['sender']) / dict_base[board][int(num)] < 0.9:
        # fail
        dict_data.setdefault('result',1)
    else:
        # pass
        dict_data.setdefault('result',0)
    print(float(dict_data['sender']))
    print(dict_base[board][int(num)])
    print(float(dict_data['sender']) / dict_base[board][int(num)])
    print(dict_data)
  
