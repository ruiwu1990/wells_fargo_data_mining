import pandas as pd
import math
import subprocess
import sys
import csv
import os
from collections import defaultdict
import json
import shutil
import numpy as np
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.mlab as mlab

app_path = os.path.dirname(os.path.abspath('__file__'))

def get_predict_observed(filename,predicted_name,observed_name):
	'''
	the function uses pandas to get the
	predicted and observed
	return a list like this [(predict0, observed0),(predict1, observed1),...]
	'''
	csv_file = pd.read_csv(filename)
	predicted = csv_file[predicted_name]
	observed = csv_file[observed_name]
	predicted_list = predicted.tolist()
	observed_list = observed.tolist()
	return [list(a) for a in zip(predicted_list, observed_list)]

# this will be '/cse/home/rwu/Desktop/machine_learning_prms_accuracy/tmp_test'
# /cse/home/rwu/Desktop/hadoop/spark_installation/spark-2.1.0/bin/pyspark

# the following construct_line and convert_csv_into_libsvm
# convert csv into libsvm
# the function is basically 
# from https://github.com/zygmuntz/phraug/blob/master/csv2libsvm.py
def construct_line( label, line ):
	new_line = []
	if float( label ) == 0.0:
		label = "0"
	new_line.append( label )

	for i, item in enumerate( line ):
		if item == '' or float( item ) == 0.0:
			continue
		new_item = "%s:%s" % ( i + 1, item )
		new_line.append( new_item )
	new_line = " ".join( new_line )
	new_line += "\n"
	return new_line

def convert_csv_into_libsvm(input_file,output_file,label_index=0,skip_headers=True):
	'''
	the function converts csv into libsvm
	'''
	i = open( input_file, 'rb' )
	o = open( output_file, 'wb' )
	reader = csv.reader( i )

	if skip_headers:
		headers = reader.next()

	for line in reader:
		if label_index == -1:
			label = '1'
		else:
			label = line.pop( label_index )

		new_line = construct_line( label, line )
		o.write( new_line )

'''
categories
1 [0,2000)
2 [2000,4000)
3 [4000,6000)
4 [6000,8000)
5 [8000,10000)
6 [10000, inf]
'''

# total_len = df.shape[0]
# df['sav_cat'] = pd.Series(np.random.randn(total_len), index=df.index)

# for i in range(total_len):
# 	# remove 2016 from time
# 	df['asof_yyyymm'][i] = df['asof_yyyymm'][i]-201600
# 	if df['sav_bal_altered'][i]>=0 and df['sav_bal_altered'][i]<10000:
# 		df['sav_cat'][i] = 1
# 	elif df['sav_bal_altered'][i]>=10000 and df['sav_bal_altered'][i]<40000:
# 		df['sav_cat'][i] = 2
# 	elif df['sav_bal_altered'][i]>=40000 and df['sav_bal_altered'][i]<6000:
# 		df['sav_cat'][i] = 3
# 	elif df['sav_bal_altered'][i]>=6000 and df['sav_bal_altered'][i]<8000:
# 		df['sav_cat'][i] = 4
# 	elif df['sav_bal_altered'][i]>=8000 and df['sav_bal_altered'][i]<10000:
# 		df['sav_cat'][i] = 5
# 	else:
# 		df['sav_cat'][i] = 6

# df.to_csv(path_or_buf='test.csv')
