#!/usr/bin/env python3
# coding: utf-8

from pexpect import pxssh
import re
import argparse

def connect_to_server(hostname, username, password):
	"""
	"""
	try:
		s = pxssh.pxssh()
		#hostname = '128.224.167.16'
		#username = 'target'
		#password = 'vxTarget'
		s.login(hostname, username, password, auto_prompt_reset=False)
		s.PROMPT='TINAC>'
		s.prompt()
		print(s.before)
		s.sendline('ps -aux | grep iperf')
		s.prompt()
		print(s.before)
		if re.search('10000', str(s.before)):
			s.sendline('pkill iperf3')
			print('kill the previous process')
			s.prompt()
			print(s.before)
		s.sendline('iperf3 -s -p 10000 -1 &')
		print('iPerf Server is listening')
		s.prompt()
		print(s.before)
		print('==logout==')
		s.logout()
	except pxssh.ExceptionPxssh as e:
		print("pxssh failed to login.")
		print(e)

if __name__ == '__main__':
	parse = argparse.ArgumentParser()
    parse.add_argument('-h', '--hostname', help='host IP address', dest='hostname', required=True)
    parse.add_argument('-u', '--username', help='username', dest='username', required=True)
    parse.add_argument('-p', '--password', help='password', dest='password', required=True)
    args = parse.parse_args()

    hostname = args.hostname
    username = args.username
    password = args.password

    connect_to_server(hostname, username, password)


