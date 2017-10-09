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
import random

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

def def_label(input_num):
	'''
	'''
	if input_num>=0 and input_num<10000:
		return 1
	elif input_num>=10000 and input_num<40000:
		return 2
	elif input_num>=40000 and input_num<100000:
		return 3
	elif input_num>=100000 and input_num<200000:
		return 4
	elif input_num>=200000 and input_num<550000:
		return 5
	else:
		return 6

def merge_same_user_salary(filename,output_file):
	'''

	'''
	fp = open(output_file, 'w')
	fp.write('mask_id,checking1,saving1,checking1_label,saving1_label,checking2,saving2,checking2_label,saving2_label,checking3,saving3,checking3_label,saving3_label,checking4,saving4,checking4_label,saving4_label,checking5,saving5,checking5_label,saving5_label,checking6,saving6,checking6_label,saving6_label\n')
	df = pd.read_csv(filename)
	mask_id = df['masked_id'].tolist()
	# mask_id = map(lambda s: s.strip(), mask_id)
	saving_money = df['sav_bal_altered'].tolist()
	# saving_money = map(lambda s: s.strip(), saving_money)
	checking_money = df['check_bal_altered'].tolist()
	# checking_money = map(lambda s: s.strip(), checking_money)
	cur_id = mask_id[0]
	tmp_row = [cur_id]
	for id_count in range(len(mask_id)):
		if  mask_id[id_count] == cur_id:
			tmp_row.append(checking_money[id_count])
			tmp_row.append(saving_money[id_count])
			tmp_row.append(def_label(checking_money[id_count]))
			tmp_row.append(def_label(saving_money[id_count]))
		else:
			# checking_label = def_label(tmp_row[-2])
			# saving_label = def_label(tmp_row[-1])
			# marking label
			fp.write(','.join([str(m) for m in tmp_row])+'\n')
			# fp.write(','.join([str(m) for m in tmp_row])+','+str(checking_label)+','+str(saving_label)+'\n')
			# print tmp_row
			cur_id = mask_id[id_count]
			tmp_row = [cur_id,checking_money[id_count],saving_money[id_count],def_label(checking_money[id_count]),def_label(saving_money[id_count])]
	fp.close()

def read_last_line(filename):
	'''
	this function reads the last 
	line of a file
	'''
	fp = open(filename,'r')
	line_list = fp.readlines()
	fp.close()
	return line_list[-1]
'''
categories
1 [0,10000)
2 [10000,40000)
3 [40000,100000)
4 [100000,200000)
5 [200000,550000)
6 [550000, inf]
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
# 	elif df['sav_bal_altered'][i]>=40000 and df['sav_bal_altered'][i]<100000:
# 		df['sav_cat'][i] = 3
# 	elif df['sav_bal_altered'][i]>=100000 and df['sav_bal_altered'][i]<200000:
# 		df['sav_cat'][i] = 4
# 	elif df['sav_bal_altered'][i]>=200000 and df['sav_bal_altered'][i]<550000:
# 		df['sav_cat'][i] = 5
# 	else:
# 		df['sav_cat'][i] = 6

# df.to_csv(path_or_buf='test.csv')
