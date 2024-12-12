import json
import sys
import os
import threading
import time
import os
import re
from gpiozero import Button 
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from time import sleep
from os import path

from DIN_block import *
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
	monitor = False

	def __init__(self):
		super().__init__()
		self._stop_event = threading.Event()
		statusdata = {}
		with open('status.json') as f:
			statusdata = json.load(f)
			if 'state' in statusdata and statusdata['state'] == 'stopped':
				self.stop()
			if 'changed' in statusdata and statusdata['changed'] == 'changed':
				self.changed = True
			if 'monitor' in statusdata and statusdata['monitor'] == 'on':
				self.monitor = True

	def stop(self):
		self._stop_event.set()
		self.monitor = False

	def getStatus(self):
		statusdata = {}
		if programThread.isRunning():
			statusdata['state'] = 'running'
		else:
			statusdata['state'] = 'stopped'
		if programThread.changed:
			statusdata['changed'] = 'changed'
		else: 
			statusdata['changed'] = 'not changed'
		if programThread.monitor:
			statusdata['monitor'] = 'on'
		else: 
			statusdata['monitor'] = 'off'
		return statusdata

	def saveStatusToFile(self):
		with open('status.json', 'w') as f:
			f.write(json.dumps(self.getStatus()))

	def isRunning(self):
		return not self._stop_event.is_set()

	def restart(self):
		self._stop_event.clear()

	def toggleMonitor(self):
		self.monitor = not self.monitor

	#Not tested yet
	def incorporateRuntimeToMonitorData(self, projectData):
		for node in projectData:
			#print(node)
			idStr = str(node["id"])
			if idStr in self.rlo:
				node["value"] = self.rlo[idStr]

			for input in node["inputs"]:
				idStr = str(input["id"])
				if idStr in self.rlo:
					input["value"] = self.rlo[idStr]
			#print(node)

		return projectData

	def incorporateMonitorDataToRuntime(self, variablesdata):
		for variable in variablesdata:
			self.mem[variable["name"]]["forced"] = variable["forced"]
			self.mem[variable["name"]]["forcedValue"] = variable["forcedValue"]

	def forceEnableOnVariable(self, varName, forceEnable):
		pass

	def forceSetOnVariable(self, varName, forcedValue):
		pass

	def run(self):
		
		while True:
		
			if os.path.isfile('listing.json') and os.path.isfile('variables.json'):
			
				self.mem = {}
				self.rlo = {}

				with open('listing.json', 'r') as file:
					listingdata = json.load(file) #parsing error accures sometimes

				with open('variables.json', 'r') as file:
					variablesdata = json.load(file)

				for var in variablesdata:
					self.mem[var["name"]] = var

				#print(self.mem)

				while not self._stop_event.is_set():
					time.sleep(1)
					print("---------------------")

					for entry in listingdata:

						if "memory" in entry and entry["memory"] != " ":

							#physical inputs
							if self.mem[entry["memory"]]["type"] in ["di"]:
								pinNum = int(re.findall(r'\d+', entry["memory"])[0])
								self.mem[entry["memory"]]["value"] = Button(pinNum)

							#overwrite mem if its forced
							if self.mem[entry["memory"]]["forced"] == True:
								self.mem[entry["memory"]]["value"] = self.mem[entry["memory"]]["forcedValue"]
								print("forcing value " + str(self.mem[entry["memory"]]["forcedValue"]) + " on variable " + entry["memory"])
							#print(self.mem)

						func = entry["function"]
						if func in globals():
							print(func + " " + str(entry["target"]))
							f_name = globals()[func]
							self.rlo = f_name(self.rlo, entry, self.mem)
							print(self.rlo)	
						
programThread = ProgramThread()
programThread.start()

@app.route('/monitor', methods=['GET'])
@cross_origin(origin='*')
def monitorProgram():
	if request.method == 'GET':
		programThread.toggleMonitor()
		programThread.saveStatusToFile()
	return jsonify(programThread.getStatus())

@app.route('/start', methods=['GET'])
@cross_origin(origin='*')
def startProgram():
	programThread.restart()
	programThread.saveStatusToFile()
	return jsonify(programThread.getStatus())

@app.route('/stop', methods=['GET'])
@cross_origin(origin='*')
def stopProgram():
	programThread.stop()
	programThread.saveStatusToFile()
	return jsonify(programThread.getStatus())

@app.route('/project', methods=['GET', 'POST'])
@cross_origin(origin='*')
def projectData():
	response_object = {}
	if request.method == 'POST':
		post_data = request.get_json()
		print('POST:', post_data)
		with open('project.json', 'w') as f:
			f.write(json.dumps(post_data))
		response_object['message'] = 'Project changed!';
		programThread.changed = True
		programThread.saveStatusToFile()
	else:
		with open('project.json') as f:
			projectdata = json.load(f)
			#print(response, file=sys.stderr)
			if programThread.monitor:
				projectdata = programThread.incorporateRuntimeToMonitorData(projectdata)
			response_object['projectdata'] = projectdata

	response_object['statusdata'] = programThread.getStatus()
	return jsonify(response_object)
	
@app.route('/variables', methods=['GET', 'POST'])
@cross_origin(origin='*')
def variablesData():
	response_object = {}
	if request.method == 'POST':
		post_data = request.get_json()
		print('POST:', post_data)
		with open('variables.json', 'w') as f:
			f.write(json.dumps(post_data))
		response_object['message'] = 'Variables changed!';
		if not programThread.monitor:
			programThread.changed = True
			programThread.saveStatusToFile()
		else:
			programThread.incorporateMonitorDataToRuntime(post_data)
	else:
		with open('variables.json') as f:
			variablesdata = json.load(f)
			#print(response, file=sys.stderr)
			response_object['variablesdata'] = variablesdata;
	response_object['statusdata'] = programThread.getStatus()
	return jsonify(response_object)

@app.route('/compile', methods=['POST'])
@cross_origin(origin='*')
def compileData():
	response_object = {}
	post_data = request.get_json()
	print('compile data:', post_data)
	with open('listing.json', 'w') as f:
		f.write(json.dumps(post_data))
	response_object['message'] = 'Compiled data saved!';
	programThread.changed = False
	programThread.saveStatusToFile();
	response_object['statusdata'] = programThread.getStatus()
	return jsonify(response_object)
	
if __name__ == '__main__':
        from waitress import serve
        serve(app, host="0.0.0.0", port=5000)

