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

	rlo = {}
	mem = {}
	changed = False

	def __init__(self):
		super().__init__()
		self._stop_event = threading.Event()

	def stop(self):
		self._stop_event.set()

	def isRunning(self):
		return not self._stop_event.is_set()

	def restart(self):
		self._stop_event.clear()

	def forceEnableOnVariable(self, varName, forceEnable):
		pass

	def forceSetOnVariable(self, varName, forcedValue):
		pass

	def run(self):
		
		while True:
		
			if os.path.isfile('listing.json') and os.path.isfile('variables.json'):
			
				self.mem = {}
				self.rlo = { "RLO" : 0, "STACK" : []}

				with open('listing.json', 'r') as file:
					listingdata = json.load(file)

				with open('variables.json', 'r') as file:
					variablesdata = json.load(file)

				for var in variablesdata:
					self.mem[var["name"]] = var

				#print(self.mem)

				while not self._stop_event.is_set():
					time.sleep(1)
					print("---------------------")

					for entry in listingdata:
						func = entry["function"]
						if func in globals():
							#print(func + " " + str(entry["target"]))
							f_name = globals()[func]
							self.rlo = f_name(self.rlo, entry, self.mem)

							#overwrite mem if its forced
							if "memory" in entry and self.mem[entry["memory"]]["forced"] == True:
								self.mem[entry["memory"]]["value"] = self.mem[entry["memory"]]["forcedValue"]
							#print(RLO_obj)	
						
programThread = ProgramThread()
programThread.start()

#@app.route('/status', methods=['GET'])
#@cross_origin(origin='*')
#def statusData():
#	response_object = {'status': 'success'}
#	#if programThread.changed:
#	#	response_object['changed'] =  'changed'
#	#else: 
#	#	response_object['changed'] =  'not changed'
#	if programThread.isRunning():
#		response_object['state'] = 'running'
#	else:
#		response_object['state'] = 'stopped'
#	return jsonify(response_object)

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
		programThread.changed = True
	else:
		with open('project.json') as f:
			projectdata = json.load(f)
			#print(response, file=sys.stderr)
			response_object['projectdata'] = projectdata
		statusdata = {'status': 'success'}
		if programThread.isRunning():
			statusdata['state'] = 'running'
		else:
			statusdata['state'] = 'stopped'
		if programThread.changed:
			statusdata['changed'] =  'changed'
		else: 
			statusdata['changed'] =  'not changed'
	response_object['statusdata'] = statusdata
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
		programThread.changed = True
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
	programThread.changed = False
	return jsonify(response_object)
	
@app.route('/monitor', methods=['GET'])
@cross_origin(origin='*')
def monitorData():
	response_object = {'status': 'success'}
	print(programThread.rlo)
	response_object['monitordata'] = programThread.rlo;
	return jsonify(response_object)
	
if __name__ == '__main__':
        from waitress import serve
        serve(app, host="0.0.0.0", port=5000)

