#!/usr/bin/env python3
# coding: utf-8
# 

from flask import Flask, render_template
from flask_pymongo import PyMongo
from collections import OrderedDict

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/iperf_db"
mongo = PyMongo(app)

def order_data(data):
	order_nightly_data = OrderedDict()
	for item in data:
		print(item['board'])
		baseline_data = mongo.db.iperf_up_bl_tb.find_one({"board":item['board']}, {'_id':0})
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
		yield order_nightly_data

@app.route('/date')
@app.route('/date/<string:date>')
def user(date=None):
	if date is None:
		datas = mongo.db.iperf_tb.find()
		return render_template('users.html', datas = datas)
	else:
		#print('=================')
		#print(date)
		nightly_data = mongo.db.iperf_up_tb.find({'run_date':date}, {'_id':0})
		order_nightly_data = order_data(nightly_data)
		#print('=================')
		#for item in order_nightly_data:
			#print(item['board'])
			
		#print("++++++++++++++++++")
		#for item in baseline_data:
			#print(item)
			#for key, value in item.items():
				#print(key, value)
		if order_nightly_data is not None:
			return render_template('users.html', datas=order_nightly_data)
		else:
			return "No data found!"

@app.route('/baseline')
def get_data():
	baseline_data = mongo.db.iperf_up_bl_tb.find({}, {'_id':0})
	return render_template('baseline.html', datas = baseline_data)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

