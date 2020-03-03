#!/usr/bin/env python3
# coding: utf-8

import subprocess
import re
from common.connect import Connect
from datetime import datetime
import time
import os

def check_board_status(barcode):
	cmd = '/folk/vlm/commandline/vlmTool getAttr -t {BARCODE} all'.format(BARCODE = barcode)
	status, result = subprocess.getstatusoutput(cmd)
	list_result = re.split(r'\n', result)
	user = list_result[-11].split(':')[-1]
	current_time = '{:%Y_%m_%d_%H_%M_%S}'.format(datetime.now())
	if not user.strip():
		insert_data(barcode, current_time, 0)
	else:
		insert_data(barcode, current_time, 1)

def insert_data(barcode, timestamp, status):
	conn = Connect.get_connection()
	mydb = conn.test
	mycol = mydb.test_tb
	mydict = {"barcode":barcode, "ts":timestamp, "status":status}
	mycol.insert_one(mydict)

def print_ts(message):
    print("[%s] %s"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message))

def run(interval, barcode):
    print_ts("-"*100)
    print_ts("Starting every %s seconds."%interval)
    print_ts("-"*100)
    while True:
        try:
            # sleep for the remaining seconds of interval
            time_remaining = interval-time.time()%interval
            print_ts("Sleeping until %s (%s seconds)..."%((time.ctime(time.time()+time_remaining)), time_remaining))
            time.sleep(time_remaining)
            print_ts("Starting command.")
            # execute the command
            #status = os.system(command)
            check_board_status(barcode)
            print_ts("-"*100)
        except Exception as e:
            print(e)


if __name__ == "__main__":
	interval = 600
	barcode = '22041'
	run(interval, barcode)
