#!/usr/bin/env python3
# coding: utf-8
# 
import os
from datetime import datetime
import argparse

def get_dvd():
	spinfile = '/net/pek-vx-system1/buildarea1/yliu2/nightly/spinReady'
	if os.path.exists(spinfile):
		with open(spinfile,'rt') as f:
			for line in f:
				testspin = line
		dvdpath = os.path.join('/net/pek-vx-system1/buildarea1/yliu2/nightly', testspin)
		return dvdpath
	else:
		print('spin not ready!')
		exit(0)

def main():
	parse = argparse.ArgumentParser()
	parse.add_argument('-p', '--plan', help='wassp test plan', dest='plan', required=True)
	args = parse.parse_args()

	wassp_plan = args.plan
	dir_name = 'log_{:%Y_%m_%d_%H_%M_%S}'.format(datetime.now())
	#dvd = '/home/windriver/DVD_Install/vxworks7'
	dvd = get_dvd()
	wassp_home = '/home/windriver/wassp-repos'
	workspace = os.path.join('/home/windriver/Workspace', dir_name)
	if not os.path.exists(workspace):
		os.makedirs(workspace)
	logs = os.path.join('/home/windriver/Logs', dir_name)
	if not os.path.exists(logs):
		os.makedirs(logs)
		os.system('ln -s {LOGS} {TARGET}'.format(LOGS = logs, TARGET = '/var/www/html'))
	command = 'runwassp -f {WASSP_PLAN} -E "WASSP_WIND_HOME={WASSP_WIND_HOME}"  -E "WASSP_HOME={WASSP_HOME}" -E "WASSP_WORKSPACE_HOME={WASSP_WORKSPACE_HOME}" -E "WASSP_LOGS_HOME={WASSP_LOGS_HOME}" --continueIfReleaseInvalid'.format(WASSP_PLAN = wassp_plan, WASSP_WIND_HOME = dvd, WASSP_HOME = wassp_home, WASSP_WORKSPACE_HOME = workspace, WASSP_LOGS_HOME = logs)
	# run wassp
	os.system(command)
	# upload test result to LTAF
	# bash ltaf_vxworks.sh -sprint Nightly  -week 2017-11-10 -ltaf vx7-SR0520-features -log /home/windriver/Logs/2017_11_10_17_24_49  -domain bsp_nightly -nightly
	sprint = 'Nightly'
	week = '{:%Y-%m-%d}'.format(datetime.now())
	release = 'vxworks_sandbox'
	domain = 'networking'
	upload_command = 'bash /home/windriver/wassp-repos/testcases/vxworks7/LTAF_meta/ltaf_vxworks.sh -sprint "{SPRINT}" -week {WEEK} -ltaf {LTAF} -log {LOG} -domain {DOMAIN} -nightly'.format(SPRINT = sprint, WEEK = week, LTAF = release, LOG = logs, DOMAIN = domain) 
	os.system(upload_command)

if __name__ == '__main__':
	main()
    
