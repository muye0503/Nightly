#!/usr/bin/env python3
# coding: utf-8
# 

from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/iperf_db"
mongo = PyMongo(app)

@app.route('/date')
@app.route('/date/<string:date>')
def user(date=None):
	if date is None:
		datas = mongo.db.iperf_tb.find()
		return render_template('users.html', datas = datas)
	else:
		#print('=================')
		#print(date)
		data = mongo.db.iperf_tb.find({'run_date':date}, {'_id':0})
		#print('=================')
		#for item in data:
			#print(type(item))
			#for key, value in item.items():
				#print(key, value)
		if data is not None:
			return render_template('users.html', datas=data)
		else:
			return "No data found!"

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')