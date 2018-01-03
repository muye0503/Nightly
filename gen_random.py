#!/usr/bin/env python3
# coding: utf-8

import random

values = range(1000000,9999999)
with open('values.csv','wt') as f:
	for i in range(1048575):
		print('{val},'.format(val = random.choice(values)), file = f)
