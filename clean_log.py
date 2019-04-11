#!/usr/bin/env python3
# coding: utf-8

import subprocess
import time
import re
import os
import shutil

def execute_local_shell_cmd(cmd):
	status, result = subprocess.getstatusoutput(cmd)
	result = result.split("\n")
	return result

def get_disk_used(disk_name):
	result = execute_local_shell_cmd("df | grep %s | awk '{print $5}'" % disk_name)
	return result[0]

def file_modify_in(file_path,time_interval='7d'):
	current_time = time.time()
	# os.path.getmtime 返回最后修改时间。返回从unix纪元开始的跳秒数
	try:
		if current_time - os.path.getmtime(file_path) < translate_time_interval_to_second(time_interval):
			return True
		return False
	except FileNotFoundError as e:
		print('FileNotFoundError:', e)

def translate_time_interval_to_second(time_interval):
	date_interval = str(time_interval.lower())
	pattern = re.compile(r'\d+')
	match = pattern.match(date_interval)
	date_interval_number = None
	if match:
		date_interval_number = int(match.group())
	else:
		raise IOError("Input {0} can't translate to second."
					  "Current support d(day)/h(hour)/m(min)/s(sec)".format(date_interval))
	if date_interval.endswith('d') or date_interval.endswith('day'):
		return date_interval_number * 24 * 3600
	elif date_interval.endswith('h') or date_interval.endswith('hour'):
		return date_interval_number * 3600
	elif date_interval.endswith('m') or date_interval.endswith('min'):
		return date_interval_number * 60
	elif date_interval.endswith('s') or date_interval.endswith('sec'):
		return date_interval_number
	else:
		raise IOError("Input {0} cant't translate to second."
					  "Current support d(day)/h(hour)/m(min)/s(second)".format(date_interval))
   
def remove_files_by_date(target_dir,before_days_remove='7d',pattern='log'):
	file_list = get_clean_log_list_by_date(target_dir,before_days_remove,pattern)
	remove_file_list(file_list)

def get_clean_log_list_by_date(target_dir,before_days_remove='7d',pattern="log"):
	before_seconds_remove = translate_time_interval_to_second(before_days_remove)
	current_time = time.time()
	# os.listdir 返回指定文件夹包含文件或文件夹的名字列表
	for candidate_file in os.listdir(target_dir):
		candidate_file_fullpath = "%s/%s" %(target_dir,candidate_file)
		# 是否存在一个普通文件
		if os.path.isfile(candidate_file_fullpath):
			candidate_file_mtime = os.path.getmtime(candidate_file_fullpath)
 
			# find\(\)根据是否包含字符串，如果包含有，返回开始的索引值，否则返回-1
			if current_time - candidate_file_mtime > before_seconds_remove \
				and candidate_file.find(pattern) != -1 \
				and not probable_current_log_file(candidate_file_fullpath):
				#  yield 就是return一个值，并且记住这个返回值的位置，下次迭代就从这个位置后开始
				yield candidate_file_fullpath

def get_clean_dir_list(path):
	for dirname in os.listdir(path):
		dir = os.path.join(path, dirname)
		print(dir)
		if not file_modify_in(dir):
			yield dir 

def remove_file(path):
	file_list = get_clean_dir_list(path)
	for file in file_list:
		if os.path.islink(file):
			print('remove link %s' %file)
			os.unlink(file)
		elif os.path.isdir(file):
			print('remove %s' %file)
			try:
		  		shutil.rmtree(file)
			except PermissionError:
		  		print('Permission denied:{0}'.format(file))
		

def get_clean_file_list(path):
	for dirpath, dirnames, filenames in os.walk(path):
		for filename in filenames:
			file = os.path.join(dirpath, filename)
			print(file)
			if not file_modify_in(file):
				yield file



if __name__ == "__main__":
	#path = '/home/windriver/Workspace'
	#path = '/home/windriver/Logs'
	#path = '/var/www/html'
	path_list = ['/home/windriver/Workspace', '/home/windriver/Logs', '/var/www/html']
	result = get_disk_used('sda1')
	pattern = re.compile(r'\d+')
	match = pattern.match(result)
	used = match.group()
	print(used)
	if int(used) >= 50:
		for dir in path_list:
			#print(dir)
			remove_file(dir)