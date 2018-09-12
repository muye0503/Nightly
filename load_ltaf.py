#!/usr/bin/env python3
# coding: utf-8

import xml.etree.ElementTree as ET
import sys
import os
import logging
import re
logging.basicConfig(level=logging.WARNING)
#logging.basicConfig(level=logging.INFO)

def parse_xml(xml_file):
	dict_node = {}
	try:
		tree = ET.parse(xml_file)
		for node in tree.iter('node'):
			logging.info(node.attrib)
			dict_node = node.attrib
		for node in tree.iter('local_info'):
			#print(node.text)
			list_str = re.split(r'[\s+]', node.text)
			list_str = list_str[867]
			print(list_str.split('=')[0], list_str.split('=')[1])
			dict_node['tags'] = list_str.split('=')[1]
			#print(list_str)
			#print(list_str[36])

		for key in dict_node:
			print(key,dict_node[key])	
		return dict_node
	except Exception as e:
		print("parse xml fail!")
		print(e)
		sys.exit()

def create_ini(xml_file):
	template = '/folk/hyan1/Nightly/result.ini'
	case_ini = 'case.ini'
	dict_node = parse_xml(xml_file)
	dict_node['Config Label'] = dict_node['config_label']
	file_data = ""
	with open(template, 'r', encoding='utf-8') as f:
		for line in f:
			if '=' in line:
				logging.info(line)
				item = line.split('=')[0]
				item_lower = item.lower().strip()
				item_lower = re.sub(r'\s+', '_', item_lower)
				logging.info(item_lower)
				#print(item, item_lower)
				if item_lower in dict_node:
					#print(item_lower, dict_node[item_lower])
					line = '{ITEM} = {VALUE} {END}'.format(ITEM = item, VALUE = dict_node[item_lower], END = os.linesep)
					logging.info(line)
					logging.info('========================')
			file_data += line 
	with open(case_ini, 'w', encoding='utf-8') as f:
		#logging.info(file_data)
		f.write(file_data)

if __name__ == '__main__':
	file = '/home/windriver/Logs/log_2018_09_12_18_27_15/p4080_18995_tcp_64/fsl_p3p4p5_platform_up/fsl_p4080_ds.BootVxBootRomfrag.Uboot.LoadVxWorks.up.fsl_common.true.gnu/testRunWorkingCopy.xml'
	parse_xml(file)
	#create_ini(file)