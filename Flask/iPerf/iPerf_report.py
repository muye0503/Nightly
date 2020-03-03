#!/usr/bin/env python3
# coding: utf-8
# 

from flask import Flask, render_template
from flask_pymongo import PyMongo
from collections import OrderedDict
import xlrd
from iPerf_result_filter import get_warning_case

app = Flask(__name__)
#app.config['MONGO_URI'] = "mongodb://128.224.153.34:27017,128.224.166.223:27107,128.224.166.211:27107/iperf_db"
#mongo = PyMongo(app)
mongo_iperf_db = PyMongo(app, uri="mongodb://128.224.153.34:27017,128.224.166.223:27107,128.224.166.211:27107/iperf_db")
mongo_baseline_db = PyMongo(app, uri="mongodb://128.224.153.34:27017,128.224.166.223:27107,128.224.166.211:27107/iperf_baseline_db")

def get_board(type):
	list_board = []
	if type == 'nightly':
		boards = '/folk/hyan1/muye0503/Nightly/Flask/iPerf/boards.xls'
	if type == 'release':
		boards = '/folk/hyan1/muye0503/Nightly/Flask/iPerf/boards_release.xls'
	rb = xlrd.open_workbook(boards,
			                formatting_info=True,
			                on_demand=True)
	ws = rb.sheet_by_index(0)
	cells_board_name = ws.col_slice(colx=0,
			          		 	start_rowx=0,
			          		 	end_rowx=100)
	for cell in cells_board_name:
		list_board.append(cell.value)
	return list_board

def order_data(data, mode, type = 'nightly'):
	# 在网页上显示时候保持板子名字有序
	order_nightly_datas = OrderedDict()
	# nightly_datas是一个临时字典
	nightly_datas = {}
	# data是从数据库中查询的结果，可以遍历。item 是一条数据记录（字典类型）
	for item in data:
		#每个板子的行记录保持有序
		order_nightly_data = OrderedDict()
		#print(item['board'])
		if mode == 'up':
			#从item中查到board, 再查询对应的baseline, baseline 不存在会报错
			baseline_data = mongo_baseline_db.db.iperf_up_bl_tb.find_one({"board":item['board']}, {'_id':0})
		if mode == 'smp':
			baseline_data = mongo_baseline_db.db.iperf_smp_bl_tb.find_one({"board":item['board']}, {'_id':0})
		if mode == 'smp_1core':
			baseline_data = mongo_baseline_db.db.iperf_smp_1core_bl_tb.find_one({"board":item['board']}, {'_id':0})
		# 遍历item 字典
		for key in item:
			order_nightly_data['board'] = item['board']
			order_nightly_data['Bits'] = item['Bits']
			order_nightly_data['BSP'] = item['BSP']
			order_nightly_data['CPU'] = item['CPU']
			order_nightly_data['Mode'] = item['Mode']
			order_nightly_data['TCP_64_bl'] = baseline_data['TCP_64']
			order_nightly_data['TCP_64'] = item['TCP_64']
			order_nightly_data['TCP_1024_bl'] = baseline_data['TCP_1024']
			order_nightly_data['TCP_1024'] = item['TCP_1024']
			order_nightly_data['TCP_65536_bl'] = baseline_data['TCP_65536']
			order_nightly_data['TCP_65536'] = item['TCP_65536']
			order_nightly_data['UDP_1400_bl'] = baseline_data['UDP_1400']
			order_nightly_data['UDP_1400'] = item['UDP_1400']
			order_nightly_data['spin'] = item['spin']
			order_nightly_data['run_date'] = item['run_date']
		nightly_datas[item['board']] = order_nightly_data
	# 添加新板子，需要加一行字典记录到order_nightly_datas
	if type == 'nightly':
		list_board = get_board('nightly')
	if type == 'release':
		list_board = get_board('release')
	for board_name in list_board:
		if board_name in nightly_datas:
			order_nightly_datas[board_name] = nightly_datas[board_name]

	return order_nightly_datas

@app.route('/date')
@app.route('/date/<string:date>')
def user(date=None):
	if date is None:
		datas = mongo_iperf_db.db.iperf_tb.find()
		return render_template('users.html', datas = datas)
	else:
		#print('=================')
		#print(date)
		nightly_data_up = mongo_iperf_db.db.iperf_up_tb.find({'run_date':date}, {'_id':0})
		order_nightly_datas_up = order_data(nightly_data_up, 'up')
		nightly_data_smp = mongo_iperf_db.db.iperf_smp_tb.find({'run_date':date}, {'_id':0})
		order_nightly_datas_smp = order_data(nightly_data_smp, 'smp')
		nightly_data_smp_1core = mongo_iperf_db.db.iperf_smp_1core_tb.find({'run_date':date}, {'_id':0})
		order_nightly_datas_smp_1core = order_data(nightly_data_smp_1core, 'smp_1core')
		#for item in order_nightly_datas:
			#print(order_nightly_datas[item]['board'])
			
		if order_nightly_datas_up is not None:
			return render_template('users.html', datas_up = order_nightly_datas_up, datas_smp = order_nightly_datas_smp, datas_smp_1core = order_nightly_datas_smp_1core)
		else:
			return "No data found!"

@app.route('/baseline')
def get_data():
	baseline_data_up = mongo_baseline_db.db.iperf_up_bl_tb.find({}, {'_id':0})
	baseline_data_smp = mongo_baseline_db.db.iperf_smp_bl_tb.find({}, {'_id':0})
	baseline_data_smp_1core = mongo_baseline_db.db.iperf_smp_1core_bl_tb.find({}, {'_id':0})
	return render_template('baseline.html', datas_up = baseline_data_up, datas_smp = baseline_data_smp, datas_smp_1core = baseline_data_smp_1core)

@app.route('/report/<string:date>')
def report(date=None):
	if date is None:
		datas = mongo_iperf_db.db.iperf_tb.find()
		return render_template('users.html', datas = datas)
	else:
		#print('=================')
		#print(date)
		#查询 run_date = date，返回所有字段除了_id
		nightly_data_up = mongo_iperf_db.db.iperf_up_tb.find({'run_date':date}, {'_id':0})
		order_nightly_datas_up = order_data(nightly_data_up, 'up')
		nightly_data_smp = mongo_iperf_db.db.iperf_smp_tb.find({'run_date':date}, {'_id':0})
		order_nightly_datas_smp = order_data(nightly_data_smp, 'smp')
		nightly_data_smp_1core = mongo_iperf_db.db.iperf_smp_1core_tb.find({'run_date':date}, {'_id':0})
		order_nightly_datas_smp_1core = order_data(nightly_data_smp_1core, 'smp_1core')
		#for item in order_nightly_datas:
			#print(order_nightly_datas[item]['board'])
			
		if order_nightly_datas_up is not None:
			return render_template('users_js.html', datas_up = order_nightly_datas_up, datas_smp = order_nightly_datas_smp, datas_smp_1core = order_nightly_datas_smp_1core)
		else:
			return "No data found!"

@app.route('/release/<string:date>')
def release(date=None):
	if date is None:
		datas = mongo_iperf_db.db.iperf_tb.find()
		return render_template('users.html', datas = datas)
	else:
		#print('=================')
		#print(date)
		#查询 run_date = date，返回所有字段除了_id
		nightly_data_up = mongo_iperf_db.db.iperf_up_tb.find({'run_date':date}, {'_id':0})
		order_nightly_datas_up = order_data(nightly_data_up, 'up', 'release')
		nightly_data_smp = mongo_iperf_db.db.iperf_smp_tb.find({'run_date':date}, {'_id':0})
		order_nightly_datas_smp = order_data(nightly_data_smp, 'smp', 'release')
		nightly_data_smp_1core = mongo_iperf_db.db.iperf_smp_1core_tb.find({'run_date':date}, {'_id':0})
		order_nightly_datas_smp_1core = order_data(nightly_data_smp_1core, 'smp_1core', 'release')
		#for item in order_nightly_datas:
			#print(order_nightly_datas[item]['board'])
			
		if order_nightly_datas_up is not None:
			return render_template('release_js.html', datas_up = order_nightly_datas_up, datas_smp = order_nightly_datas_smp, datas_smp_1core = order_nightly_datas_smp_1core)
		else:
			return "No data found!"

@app.route('/warning/<string:date>')
def warning(date=None):
	res = get_warning_case(date)
	#print(res)
	if date is not None:
		return render_template('warning.html', datas = res)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

