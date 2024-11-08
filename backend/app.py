import json
import sys
import os
import threading
import time
import os
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from time import sleep
from os import path

from AND_block import *
from OR_block import *
from ASSIGN_block import *

app = Flask(__name__)
#CORS(app, origins=["http://localhost:80","http://localhost:80"])
#CORS(app, resources={r"/project": {"origins": "http://localhost:80"}})

@app.route('/')
def index():
    return 'Hello, World!'

class ProgramThread(threading.Thread):

	RLO_obj = { "RLO" : 0, "STACK" : []}
	mem = {}

	def __init__(self):
		super().__init__()
		self._stop_event = threading.Event()

	def stop(self):
		self._stop_event.set()

	def restart(self):
		self._stop_event.clear()

	def forceVariableOnline(self, variable):
		#Update only forced, forcedValue, 
		pass

	def run(self):
		
		while True:
		
			if os.path.isfile('listing.json') and os.path.isfile('variables.json'):
			
				with open('listing.json', 'r') as file:
					listingdata = json.load(file)

				with open('variables.json', 'r') as file:
					variablesdata = json.load(file)

				for var in variablesdata:
					self.mem[var["name"]] = var

				print(self.mem)

				while not self._stop_event.is_set():

					time.sleep(3)
					print("---------------------")
					#os.system('cls')
					for func in listingdata:
						value = func["function"]
						if value in globals():
							print(value + " " + str(func["target"]))
							f_name = globals()[value]
							self.RLO_obj = f_name(self.RLO_obj, func, self.mem)
							#print(RLO_obj)	
						
programThread = ProgramThread()
programThread.start()

@app.route('/start', methods=['GET'])
@cross_origin(origin='*')
def startProgram():
	programThread.restart()
	return jsonify({'status':'success'})

@app.route('/stop', methods=['GET'])
@cross_origin(origin='*')
def stopProgram():
	programThread.stop()
	return jsonify({'status':'success'})

@app.route('/project', methods=['GET', 'POST'])
@cross_origin(origin='*')
def projectData():
	response_object = {'status': 'success'}
	if request.method == 'POST':
		post_data = request.get_json()
		print('POST:', post_data)
		with open('project.json', 'w') as f:
			f.write(json.dumps(post_data))
		response_object['message'] = 'Project changed!';
	else:
		with open('project.json') as f:
			projectdata = json.load(f)
			#print(response, file=sys.stderr)
			response_object['projectdata'] = projectdata;
	return jsonify(response_object)
	
@app.route('/variables', methods=['GET', 'POST'])
@cross_origin(origin='*')
def variablesData():
	response_object = {'status': 'success'}
	if request.method == 'POST':
		post_data = request.get_json()
		print('POST:', post_data)
		with open('variables.json', 'w') as f:
			f.write(json.dumps(post_data))
		response_object['message'] = 'Variables changed!';
	else:
		with open('variables.json') as f:
			variablesdata = json.load(f)
			#print(response, file=sys.stderr)
			response_object['variablesdata'] = variablesdata;
	return jsonify(response_object)

@app.route('/compile', methods=['POST'])
@cross_origin(origin='*')
def compileData():
	response_object = {'status': 'success'}
	post_data = request.get_json()
	print('compile data:', post_data)
	with open('listing.json', 'w') as f:
		f.write(json.dumps(post_data))
	response_object['message'] = 'Compiled data saved!';
	return jsonify(response_object)
	
@app.route('/monitor', methods=['GET'])
@cross_origin(origin='*')
def monitorData():
	pass;
	
if __name__ == '__main__':
        from waitress import serve
        serve(app, host="0.0.0.0", port=5000)

