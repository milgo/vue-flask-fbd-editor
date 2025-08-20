import json
import sys
import os
import threading
import time
import os
import re
from gpiozero import Button, LED
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from time import sleep
from os import path

from DIN_block import *
from CONST_block import *
from AND_block import *
from OR_block import *
from NOT_block import *
from ASSIGN_block import *
from MOVE_block import *
from S_block import *
from R_block import *
from SR_block import *
from RS_block import *
from SP_block import *
from SE_block import *
from SD_block import *
from SS_block import *
from SF_block import *
from CU_block import *
from CD_block import *
from EQ_block import *
from GT_block import *
from LT_block import *
from GE_block import *
from LE_block import *
from ADD_block import *
from SUB_block import *
from MUL_block import *
from DIV_block import *
from TIME_block import *

app = Flask(__name__)
#CORS(app, origins=["http://localhost:80","http://localhost:80"])
#CORS(app, resources={r"/project": {"origins": "http://localhost:80"}})

@app.route('/')
def index():
    return 'Hello, World!'

class ProgramThread(threading.Thread):

	rlo = {}
	mem = {}
	variablesdata = {}
	projectdata = {}
	do = {}
	di = {}
	
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
		with open('project.json') as f:
			self.projectdata = json.load(f)
		with open('variables.json', 'r') as file:
			self.variablesdata = json.load(file)

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
	def getNodesAndInputsValuesInProjectData(self, projectData):
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

	def getVariablesValuesInVariablesData(self, variablesData):
		for variable in variablesData:
			variable["value"] = self.mem[variable["name"]]["value"]
		return variablesData

	def forceVariables(self, variablesdata):
		for variable in variablesdata:
			self.mem[variable["name"]]["forced"] = variable["forced"]
			self.mem[variable["name"]]["forcedValue"] = variable["forcedValue"]

	def forceEnableOnVariable(self, varName, forceEnable):
		pass

	def forceSetOnVariable(self, varName, forcedValue):
		pass

	def run(self):
        
		self.do["%o21"] = LED(21)
		self.di["%i22"] = Button(22)
		while True:
		
			if os.path.isfile('listing.json') and os.path.isfile('variables.json') and os.path.isfile('project.json') and not self._stop_event.is_set():
			
				self.mem = {}
				self.rlo = {}

				with open('project.json') as f:
					self.projectdata = json.load(f)

				with open('variables.json', 'r') as file:
					self.variablesdata = json.load(file)
					
				with open('listing.json', 'r') as file:
					listingdata = json.load(file)

				for var in self.variablesdata:
					self.mem[var["name"]] = var

				for setupentry in listingdata[0]['setuplisting']:
					setupfunc = setupentry["functionName"]
					print(setupfunc + " " + str(setupentry["id"]))
					if setupfunc in globals():						
						f_ptr = globals()[setupfunc]
						f_ptr(setupentry, self.mem)
						#print(self.rlo)
						#print(self.mem)

				while not self._stop_event.is_set():
					time.sleep(0.1)
					#print("---------------------")

					for entry in listingdata[0]['listing']:

						if "memoryAddr" in entry and entry["memoryAddr"] != " ":

							#physical inputs
							if self.mem[entry["memoryAddr"]]["type"] in ["di"]:
								#pinNum = int(re.findall(r'\d+', entry["memory"])[0])
								if entry["memoryAddr"] in self.di:
									if self.di[entry["memoryAddr"]].is_pressed == True:
										self.mem[entry["memoryAddr"]]["value"] = 1
									else:
										self.mem[entry["memoryAddr"]]["value"] = 0

							if self.mem[entry["memoryAddr"]]["type"] in ["do"]:
								if entry["memoryAddr"] in self.do:									
									if self.mem[entry["memoryAddr"]]["value"] == 1:
										self.do[entry["memoryAddr"]].on()
									else:
										self.do[entry["memoryAddr"]].off()

							#overwrite mem if its forced
							if self.mem[entry["memoryAddr"]]["forced"] == True:
								self.mem[entry["memoryAddr"]]["value"] = self.mem[entry["memoryAddr"]]["forcedValue"]
								#print("forcing value " + str(self.mem[entry["memory"]]["forcedValue"]) + " on variable " + entry["memory"])
							
						print(self.mem)
						print("--------------")
						print(self.rlo)
						func = entry["functionName"]
						if func in globals():
							#print(func + " " + str(entry["target"]))
							f_ptr = globals()[func]
							self.rlo = f_ptr(self.rlo, entry, self.mem)
							#print(self.rlo)
						
programThread = ProgramThread()
programThread.start()

@app.route('/monitor', methods=['GET'])
@cross_origin(origin='*')
def monitorProgram():
	if request.method == 'GET':
		if programThread.isRunning():
			programThread.toggleMonitor()
			programThread.saveStatusToFile()
	return jsonify(programThread.getStatus())

@app.route('/forcevariables', methods=['POST'])
@cross_origin(origin='*')
def forceVariables():
	response_object = {}
	if request.method == 'POST':
		if programThread.isRunning():
			post_data = request.get_json()
			programThread.forceVariables(post_data)
			response_object['variablesdata'] = programThread.variablesdata
	response_object['statusdata'] = programThread.getStatus()
	return jsonify(response_object)

@app.route('/pullruntimedata', methods=['GET'])
@cross_origin(origin='*')
def pullRuntimeData():
	response_object = {}
	if request.method == 'GET':
		if programThread.isRunning():
			response_object['variablesdata'] = programThread.getVariablesValuesInVariablesData(programThread.variablesdata)
			response_object['projectdata'] = programThread.getNodesAndInputsValuesInProjectData(programThread.projectdata)
	response_object['statusdata'] = programThread.getStatus()
	return jsonify(response_object)

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
		if not programThread.isRunning():
			post_data = request.get_json()
			#print('POST:', post_data)
			with open('project.json', 'w') as f:
				f.write(json.dumps(post_data))
			response_object['message'] = 'Project changed!';
			programThread.projectdata = post_data #!!!
			programThread.changed = True
			programThread.saveStatusToFile()
	else:
		response_object['projectdata'] = programThread.projectdata
	response_object['statusdata'] = programThread.getStatus()
	return jsonify(response_object)
	
@app.route('/variables', methods=['GET', 'POST'])
@cross_origin(origin='*')
def variablesData():
	response_object = {}
	if request.method == 'POST':
		if not programThread.isRunning():
			post_data = request.get_json()
			for var in post_data:
				var["edit"] = False
			#print('POST:', post_data)
			with open('variables.json', 'w') as f:
				f.write(json.dumps(post_data))
			response_object['message'] = 'Variables changed!';
			programThread.variablesdata = post_data
			programThread.changed = True
			programThread.saveStatusToFile()
	else:
		response_object['variablesdata'] = programThread.variablesdata;
	response_object['statusdata'] = programThread.getStatus()
	return jsonify(response_object)

@app.route('/compile', methods=['POST'])
@cross_origin(origin='*')
def compileData():
	response_object = {}
	if not programThread.isRunning():
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


