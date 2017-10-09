from flask import Flask, render_template, send_from_directory, request
import util, os, subprocess
# import shutil
# import time
app = Flask(__name__)

app_path = os.path.dirname(os.path.abspath(__file__))
# should be set in the configuration file
data_file = 'data/test.csv'
input_file = 'data/test.libsvm'

# remove when dokerize
spark_submit_location = '/home/host0/Desktop/hadoop/spark-2.1.0/bin/spark-submit'

@app.route('/')
def index():
	return render_template('index.html')
	# return render_template('wf-dynamic-ad/src/index.html')

@app.route('/api/predict/<previous_saving_account>')
def predict_next_month(previous_saving_account=''):
	'''
	previous_saving_account should contains previous five month
	saving account info and seperated by +
	'''
	saving_list = previous_saving_account.strip().split('+')
	print saving_list
	if len(saving_list) != 5:
		return "Sorry, the saving info has something wrong. It should have 5 month info"
	else:
		saving_list = [float(i) for i in saving_list]
		saving_list =[util.def_label(i) for i in saving_list]
		saving_str = '+'.join([str(i) for i in saving_list])
		util.convert_csv_into_libsvm(data_file,input_file)
		input_data_loc = input_file
		# execute models
		log_path = 'results/random_forest.log'
		err_log_path = 'results/random_forest_err.log'
		exec_file_loc = 'ml_model/random_forest.py'
		command = [spark_submit_location, exec_file_loc, input_data_loc, saving_str]
		with open(log_path, 'wb') as process_out, open(log_path, 'rb', 1) as reader, open(err_log_path, 'wb') as err_out:
			process = subprocess.Popen(
				command, stdout=process_out, stderr=err_out, cwd=app_path)
		# wait until the process finishes
		process.wait()
		return util.read_last_line(log_path)

@app.route('/api/cross_validation')
def cross_validation():
	'''
	this api returns our model 20-time cross validation
	results
	'''
	# convert files
	util.convert_csv_into_libsvm(data_file,input_file)
	input_data_loc = input_file
	# execute models
	log_path = 'results/random_forest.log'
	err_log_path = 'results/random_forest_err.log'
	exec_file_loc = 'ml_model/random_forest_cross_validation.py'
	command = [spark_submit_location, exec_file_loc, input_data_loc]
	with open(log_path, 'wb') as process_out, open(log_path, 'rb', 1) as reader, open(err_log_path, 'wb') as err_out:
		process = subprocess.Popen(
			command, stdout=process_out, stderr=err_out, cwd=app_path)
	# wait until the process finishes
	process.wait()
	return util.read_last_line(log_path)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')