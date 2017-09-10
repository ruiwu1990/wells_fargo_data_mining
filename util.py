import pandas as pd
import math
import subprocess
import sys
import csv
import os
from collections import defaultdict
import json

app_path = os.path.dirname(os.path.abspath(__file__))

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
