#!/usr/bin/env python3
# coding: utf-8
# 
import os
from datetime import datetime
import argparse

def main():
	parse = argparse.ArgumentParser()
	parse.add_argument('--plan', help='wassp test plan', dest='plan', required=True)
	parse.add_argument('--dvd', help='the spin to test', dest='dvd', required=True)
	parse.add_argument('--rundate', help='rundate', dest='rundate', required=True)
	parse.add_argument('--release', help='ltaf release', dest='release', required=True)
	args = parse.parse_args()
	wassp_plan = args.plan
	dir_name = 'log_{:%Y_%m_%d_%H_%M_%S}'.format(datetime.now())
	dvd = args.dvd
	wassp_home = '/home/windriver/wassp-repos'
	workspace = os.path.join('/home/windriver/Workspace', dir_name)
	if not os.path.exists(workspace):
		os.makedirs(workspace)
	logs = os.path.join('/home/windriver/Logs', dir_name)
	if not os.path.exists(logs):
		os.makedirs(logs)
		os.system('ln -s {LOGS} {TARGET}'.format(LOGS = logs, TARGET = '/var/www/html'))
	if os.path.exists('/home/windriver/tmp/rerun_parameters.sh'):
		os.remove('/home/windriver/tmp/rerun_parameters.sh')
	with open('/home/windriver/tmp/rerun_parameters.sh', 'wt') as f: 
		print('log_path={LOGS}'.format(LOGS = logs), file = f)
		print('plan={PLAN}'.format(PLAN = wassp_plan), file = f)
		print('workspace={WORKSPACE}'.format(WORKSPACE = workspace), file = f)
	command = 'runwassp -f {WASSP_PLAN} -E "WASSP_WIND_HOME={WASSP_WIND_HOME}"  -E "WASSP_HOME={WASSP_HOME}" -E "WASSP_WORKSPACE_HOME={WASSP_WORKSPACE_HOME}" -E "WASSP_LOGS_HOME={WASSP_LOGS_HOME}" --continueIfReleaseInvalid'.format(WASSP_PLAN = wassp_plan, WASSP_WIND_HOME = dvd, WASSP_HOME = wassp_home, WASSP_WORKSPACE_HOME = workspace, WASSP_LOGS_HOME = logs)
	# run wassp
	os.system(command)
	# upload test result to LTAF
	# bash ltaf_vxworks.sh -sprint Nightly  -week 2017-11-10 -ltaf vx7-SR0520-features -log /home/windriver/Logs/2017_11_10_17_24_49  -domain bsp_nightly -nightly
	sprint = 'Nightly'
	#week = '{:%Y-%m-%d}'.format(datetime.now())
	week = args.rundate
	#/net/pek-vx-nightly1/buildarea1/pzhang1/jenkinsEnvInjection/vx7_nightly_spin.config
	#release = args.release
	release = 'vxworks_sandbox'
	domain = 'networking'
	upload_command = 'bash /home/windriver/wassp-repos/testcases/vxworks7/LTAF_meta/ltaf_vxworks.sh -sprint "{SPRINT}" -week {WEEK} -ltaf {LTAF} -log {LOG} -domain {DOMAIN} -nightly'.format(SPRINT = sprint, WEEK = week, LTAF = release, LOG = logs, DOMAIN = domain) 
	os.system(upload_command)

if __name__ == '__main__':
	main()
    
