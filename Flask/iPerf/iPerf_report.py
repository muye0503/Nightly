#!/usr/bin/env python3
# coding: utf-8
# 

from flask import Flask, render_template
from flask_pymongo import PyMongo
from collections import OrderedDict

app = Flask(__name__)
#app.config['MONGO_URI'] = "mongodb://localhost:27017/iperf_db"
app.config['MONGO_URI'] = "mongodb://128.224.153.34:27017/iperf_db"
mongo = PyMongo(app)

def order_data(data, mode):
	order_nightly_datas = OrderedDict()
	nightly_datas = {}
	for item in data:
		order_nightly_data = OrderedDict()
		#print(item['board'])
		if mode == 'up':
			baseline_data = mongo.db.iperf_up_bl_tb.find_one({"board":item['board']}, {'_id':0})
		if mode == 'smp':
			baseline_data = mongo.db.iperf_smp_bl_tb.find_one({"board":item['board']}, {'_id':0})
		if mode == 'smp_1core':
			baseline_data = mongo.db.iperf_smp_1core_bl_tb.find_one({"board":item['board']}, {'_id':0})
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
	if 'idpQ35-18180' in nightly_datas:
		order_nightly_datas['idpQ35-18180'] = nightly_datas['idpQ35-18180']
	if 'fsl_p4080_ds-18995' in nightly_datas:
		order_nightly_datas['fsl_p4080_ds-18995'] = nightly_datas['fsl_p4080_ds-18995']
	if 'fsl_imx6_sabrelite-25005' in nightly_datas:
		order_nightly_datas['fsl_imx6_sabrelite-25005'] = nightly_datas['fsl_imx6_sabrelite-25005']
	if 'TI_keystone2_K2E-28384' in nightly_datas:
		order_nightly_datas['TI_keystone2_K2E-28384'] = nightly_datas['TI_keystone2_K2E-28384']
	if 'xilinx_zynq7k_zc706-28385' in nightly_datas:
		order_nightly_datas['xilinx_zynq7k_zc706-28385'] = nightly_datas['xilinx_zynq7k_zc706-28385']
	if 'fsl_P2020RDB-18491' in nightly_datas:
		order_nightly_datas['fsl_P2020RDB-18491'] = nightly_datas['fsl_P2020RDB-18491']
	if 'XILINX_ZCU102-25087' in nightly_datas:
		order_nightly_datas['XILINX_ZCU102-25087'] = nightly_datas['XILINX_ZCU102-25087']
	if 'fsl_T2080QDS-22041' in nightly_datas:
		order_nightly_datas['fsl_T2080QDS-22041'] = nightly_datas['fsl_T2080QDS-22041']
	if 'TI_AM335x_EVM-22599' in nightly_datas:
		order_nightly_datas['TI_AM335x_EVM-22599'] = nightly_datas['TI_AM335x_EVM-22599']
	if 'fsl_LS1021A_TWR-28380' in nightly_datas:
		order_nightly_datas['fsl_LS1021A_TWR-28380'] = nightly_datas['fsl_LS1021A_TWR-28380']
	if 'fsl_VF610_TWR-24601' in nightly_datas:
		order_nightly_datas['fsl_VF610_TWR-24601'] = nightly_datas['fsl_VF610_TWR-24601']
	if 'idpQ35-18202' in nightly_datas:
		order_nightly_datas['idpQ35-18202'] = nightly_datas['idpQ35-18202']
	if 'Q170-28512' in nightly_datas:
		order_nightly_datas['Q170-28512'] = nightly_datas['Q170-28512']
	if 'idpQ35-18180-32' in nightly_datas:
		order_nightly_datas['idpQ35-18180-32'] = nightly_datas['idpQ35-18180-32']
	if 'Cyclone-21989' in nightly_datas:
		order_nightly_datas['Cyclone-21989'] = nightly_datas['Cyclone-21989']
	if 'fsl_LS1043A_RDB_PC-25064' in nightly_datas:
		order_nightly_datas['fsl_LS1043A_RDB_PC-25064'] = nightly_datas['fsl_LS1043A_RDB_PC-25064']
	if 'fsl_LS1043A_RDB_PC-25064-32' in nightly_datas:
		order_nightly_datas['fsl_LS1043A_RDB_PC-25064-32'] = nightly_datas['fsl_LS1043A_RDB_PC-25064-32']
	if 'TI_keystone2_K2E-28384-IP' in nightly_datas:
		order_nightly_datas['TI_keystone2_K2E-28384-IP'] = nightly_datas['TI_keystone2_K2E-28384-IP']

	return order_nightly_datas

@app.route('/date')
@app.route('/date/<string:date>')
def user(date=None):
	if date is None:
		datas = mongo.db.iperf_tb.find()
		return render_template('users.html', datas = datas)
	else:
		#print('=================')
		#print(date)
		nightly_data_up = mongo.db.iperf_up_tb.find({'run_date':date}, {'_id':0})
		order_nightly_datas_up = order_data(nightly_data_up, 'up')
		nightly_data_smp = mongo.db.iperf_smp_tb.find({'run_date':date}, {'_id':0})
		order_nightly_datas_smp = order_data(nightly_data_smp, 'smp')
		nightly_data_smp_1core = mongo.db.iperf_smp_1core_tb.find({'run_date':date}, {'_id':0})
		order_nightly_datas_smp_1core = order_data(nightly_data_smp_1core, 'smp_1core')
		#for item in order_nightly_datas:
			#print(order_nightly_datas[item]['board'])
			
		if order_nightly_datas_up is not None:
			return render_template('users_js.html', datas_up = order_nightly_datas_up, datas_smp = order_nightly_datas_smp, datas_smp_1core = order_nightly_datas_smp_1core)
		else:
			return "No data found!"

@app.route('/baseline')
def get_data():
	baseline_data_up = mongo.db.iperf_up_bl_tb.find({}, {'_id':0})
	baseline_data_smp = mongo.db.iperf_smp_bl_tb.find({}, {'_id':0})
	baseline_data_smp_1core = mongo.db.iperf_smp_1core_bl_tb.find({}, {'_id':0})
	return render_template('baseline.html', datas_up = baseline_data_up, datas_smp = baseline_data_smp, datas_smp_1core = baseline_data_smp_1core)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

