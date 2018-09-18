#!/usr/bin/env python3
# coding: utf-8

import os
import logging
import argparse
logging.basicConfig(level=logging.WARNING)

def find_case(**kw):
	#logdir = '/home/windriver/wassp-repos/testcases/vxworks7/networking/IPERF_UP/'
	logdir = kw['log']
	for dir in os.listdir(logdir):
		dir_path = os.path.join(logdir, dir)
		if os.path.isdir(dir_path):
			logging.info(dir_path)
			create_conf(dir_path, logdir.split('/')[-1], **kw)


def create_conf(dir, suite, **kw):

	template = '/folk/hyan1/Nightly/test_case.conf'
	case_name = dir.split('/')[-1]
	case_conf = os.path.join(dir, 'test_case.conf')
	d_conf = {}
	d_conf.setdefault('RELEASE_NAME', '')
	d_conf['TEST_SUITE_NAME'] = suite
	d_conf['COMPONENT'] = 'networking'
	d_conf['TEST_CASE_TYPE'] = 'Performance'
	d_conf['FEATURE'] = 'IPERF'
	d_conf['AUTOMATION'] = 'yes'
	d_conf['RCA'] = 'no'
	d_conf['DESCRIPTION'] = '"networking test for L4 performance"'
	d_conf['TRACEABILITY'] = 'F7641'
	d_conf['TEST_CASE_LIST'] = '"{CASE_NAME}"'.format(CASE_NAME = case_name)
	d_conf['GIT_LINK'] = '"http://git.wrs.com/cgit/projects/wassp-repos/testcases/vxworks7/tree/networking/{SUITE}"'.format(SUITE = suite)
	d_conf['CREATED_DATE'] = '2018-9-14'
	if 'release' in kw:
		d_conf['RELEASE_NAME'] = kw['release']
	file_data = ""
	with open(template, 'r', encoding='utf-8') as f:
		for line in f:
			if '=' in line:
				logging.info(line)
				item = line.split('=')[0].strip()
				logging.info(item)
				#print(item, item_lower)
				if item in d_conf:
					#print(item_lower, dict_node[item_lower])
					line = '{ITEM} = {VALUE} {END}'.format(ITEM = item, VALUE = d_conf[item], END = os.linesep)
					logging.info(line)
					logging.info('========================')
			file_data += line 

	with open(case_conf, 'w', encoding='utf-8') as f:
		f.write(file_data)
	if 'release' in kw:
		logging.info(case_conf)
		command = 'curl -F testfile=@{FILE} http://pek-lpgtest3.wrs.com/ltaf/upload_test.php'.format(FILE = case_conf)
		os.system(command)

def main():
	parse = argparse.ArgumentParser()
	parse.add_argument('--log', help='log path', dest='log', required=True)
	parse.add_argument('--release', help='ltaf release', dest='release', required=False)
	args = parse.parse_args()
	p_log = args.log
	p_release = args.release
	kw = {}
	if p_log:
		kw['log'] = p_log
	if p_release:
		kw['release'] = p_release

	find_case(**kw)

if __name__ == "__main__":
	main()