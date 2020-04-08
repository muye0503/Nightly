#!/usr/bin/env python3
# coding: utf-8

import os
from lxml import etree
from selenium import webdriver
from LTAF_nightly_2_release import Case
import time
import argparse
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
		
class WarningCase(Case):
	"""docstring for ClassName"""
	def __init__(self, arg):
		self.me = arg.xpath('.//text()')
		self.boardname = arg.xpath('.//..//td[2]/text()')
		self.bits = arg.xpath('.//..//td[3]/text()')
		self.cpu = arg.xpath('.//..//td[5]/text()')
		self.mode = arg.xpath('.//..//td[6]/text()')
		self.tcp_64 = arg.xpath('.//..//td[8]/text()')
		self.tcp_1024 = arg.xpath('.//..//td[10]/text()')
		self.tcp_65536 = arg.xpath('.//..//td[12]/text()')
		self.udp_1400 = arg.xpath('.//..//td[14]/text()')

	def display_result(self):
		super().set_attr_tostring()
		list_result = [
			self.boardname,
			self.bits,
			self.cpu,
			self.mode
		]
		#print(type(self.udp_1400))
		dict_result = {
			self.tcp_64 : 'TCP_64',
			self.tcp_1024 : 'TCP_1024',
			self.tcp_65536 : 'TCP_65536',
			self.udp_1400 : 'UDP_1400'
		}

		if self.me in dict_result:
			list_result.append(dict_result[self.me])
			list_result.append(self.me)
		return list_result
		#print(list_result)

class Result(object):
	def __init__(self, source):
		self.source = source

	def get_result(self):
		html = etree.HTML(self.source)
		cases = html.xpath('//td[@style="color: rgb(255, 165, 0);"]')
		#cases = html.xpath('//td[@style="color: rgb(255, 165, 0);"]/..//td[2]/text()')
		#cases = html.xpath('//td[@class="baseline"]/text()')
		return cases

def screen_short(date, capture_type=None):
	#SCREEN_PATH = '/net/pek-vx-nwk1/buildarea1/hyan1/ScreenShort'
	SCREEN_PATH = '/folk/hyan1/Nightly/nightlyReport'
	#chrome_options = webdriver.ChromeOptions()
	#chrome_options.add_argument('--headless')
	#chrome_options.add_argument('--hide-scrollbars')
	#browser =webdriver.Chrome(options = chrome_options)
	#browser.get('http://pek-vx-nwk1/report/{}'.format(date))
	options = webdriver.FirefoxOptions()
	options.add_argument('-headless')
	browser = webdriver.Firefox(executable_path='/buildarea1/hyan1/flask/geckodriver', firefox_options=options)
	browser.get('http://pek-vx-nwk1/warning/{}'.format(date))
	#print(browser.page_source)
	wait = WebDriverWait(browser, 20)
	item = wait.until(EC.presence_of_element_located((By.ID, 'up')))
	#time.sleep(2)
	# generate pdf
	#google-chrome --headless --disable-gpu --print-to-pdf=sreenshort_2020-02-28.pdf http://pek-vx-nwk1/report/2020-02-28
	
	width = browser.execute_script("return document.documentElement.scrollWidth")
	height = browser.execute_script("return document.documentElement.scrollHeight")
	browser.set_window_size(width, height)
	time.sleep(2)
	#browser.save_screenshot('{}/sreenshort_{}_{}.png'.format(SCREEN_PATH, capture_type, date))
	browser.save_screenshot('{}/sreenshort_warning_cases.png'.format(SCREEN_PATH))
	browser.close()

def get_warning_case(date):
	#chrome_options = webdriver.ChromeOptions()
	#chrome_options.add_argument('--headless')
	#browser = webdriver.Chrome(options = chrome_options)

	options = webdriver.FirefoxOptions()
	options.add_argument('-headless')
	browser = webdriver.Firefox(executable_path='/buildarea1/hyan1/flask/geckodriver', firefox_options=options)
	browser.get('http://pek-vx-nwk1/report/{}'.format(date))
	wait = WebDriverWait(browser, 20)
	item = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//td[@style="color: rgb(255, 165, 0);"]')))
	page_source = browser.page_source
	#time.sleep(5)
	#print(page_source)
	nightly_result = Result(page_source)
	#print(nightly_result.get_result())
	waring_result = nightly_result.get_result()
	#print(waring_result)
	list_result = []
	for result in waring_result:
		#print(result)
		case = WarningCase(result)
		#case.get_attr()
		warning_case = case.display_result()
		list_result.append(warning_case)
	#print(list_result)
	browser.close()
	return list_result

def time_delta(run_date):
    y = datetime.strptime(run_date, '%Y-%m-%d')
    z = datetime.now()
    diff = z - y
    return diff.days - 1	

if __name__ == '__main__':
	parse = argparse.ArgumentParser()
	parse.add_argument('--run_date', help='run date', dest='run_date', required=True)
	args = parse.parse_args()
	date = args.run_date
	if time_delta(date) <= 0:
		screen_short(date)
