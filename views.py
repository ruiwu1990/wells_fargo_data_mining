from flask import Flask, render_template, send_from_directory, request
import util
import os
# import shutil
# import time
app = Flask(__name__)

app_path = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
	return render_template('index.html')
	# return render_template('wf-dynamic-ad/src/index.html')

@app.route('/api/test')
def test():
	'''
	test
	'''
	return 'test'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')