#!/usr/bin/env python3
# coding: utf-8

import argparse
from collections import defaultdict

dict_base = defaultdict(list)
# p2020_18491 tcp_64 141 142 141 142 141
dict_base['p2020_18491'].append(139)
# p2020_18491 tcp_1024 921 912 915 928 932
dict_base['p2020_18491'].append(900)
# p2020_18491 tcp_65536 940 940 940 940 940
dict_base['p2020_18491'].append(940)
# p2020_18491 udp_1400 617 615 614 617 627
dict_base['p2020_18491'].append(515)
# zynq7k_19908 tcp_64 
dict_base['zynq7k_19908'].append(93.1)
# zynq7k_19908 tcp_1024 
dict_base['zynq7k_19908'].append(383)
# zynq7k_19908 tcp_65536
dict_base['zynq7k_19908'].append(503)
# zynq7k_19908 udp_1400
dict_base['zynq7k_19908'].append(0.65)
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
dict_base['am335x_22599'].append(22.3)
# am335x_22599 tcp_1024 157 158 156 158 158
dict_base['am335x_22599'].append(150)
# am335x_22599 tcp_65536 414 414 411 417 417
dict_base['am335x_22599'].append(408)
# am335x_22599 udp_1400 225 225 225 227 227
dict_base['am335x_22599'].append(226)
# imx6_25005 tcp_64 106 106 106 107 107
dict_base['imx6_25005'].append(106)
# imx6_25005 tcp_1024 345 346 346 350 349
dict_base['imx6_25005'].append(348)
# imx6_25005 tcp_65536 409 410 413 423 426
dict_base['imx6_25005'].append(427)
# imx6_25005 udp_1400 460 460 460 460 460
dict_base['imx6_25005'].append(460)
# idpQ35_18180 tcp_64 413 415 411 415
dict_base['idpQ35_18180'].append(404)
# idpQ35_18180 tcp_1024 902 940 874 869
dict_base['idpQ35_18180'].append(731)
# idpQ35_18180 tcp_65536 940 888 940
dict_base['idpQ35_18180'].append(940)
# idpQ35_18180 udp_1400 955 955 955 955
dict_base['idpQ35_18180'].append(955)

def get_throughput(log):
    """
    """

    dict_data = {}
    with open(log,'r') as f:
        for line in f:
            line = line.strip()
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
  
