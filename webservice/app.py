import json
import sys
import os
import threading
import time
import os
import re
from gpiozero import Button, LED
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS, cross_origin
from time import sleep
from os import path
import hashlib

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
from FP_block import *
from FN_block import *
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
    return send_from_directory('dist', 'index.html')

@app.route('/assets/plugin.js')
def script():
    return send_from_directory('dist/assets', 'plugin.js')

@app.route('/assets/index.css')
def style():
    return send_from_directory('dist/assets', 'index.css')

@app.route('/assets/warning.png')
def warningSign():
    return send_from_directory('dist/assets', 'warning.png')

class ProgramThread(threading.Thread):

	rlo = {}
	mem = {}
	#variablesdata = {}
	projectdata = {}
	checksum = ""
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
		#with open('variables.json', 'r') as file:
		#	self.variablesdata = json.load(file)

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

		statusdata['checksum'] = self.getProjectdataChecksum(self.projectdata)
		return statusdata

	def getProjectdataChecksum(self, projectData):
		hashObject = hashlib.md5(json.dumps(projectData).encode())
		return hashObject.hexdigest()

	def saveStatusToFile(self):
		with open('status.json', 'w') as f:
			f.write(json.dumps(self.getStatus()))

	def isRunning(self):
		return not self._stop_event.is_set()

	def restart(self):
		self._stop_event.clear()

	def toggleMonitor(self):
		self.monitor = not self.monitor

	def pullRuntimeValuesToProjectData(self, projectData):
		for node in projectData["program"]:
			#print(node)
			idStr = str(node["id"])
			if idStr in self.rlo:
				node["value"] = self.rlo[idStr]

			for input in node["inputs"]:
				idStr = str(input["id"])
				if idStr in self.rlo:
					input["value"] = self.rlo[idStr]

		for variable in projectData["variables"]:
			variable["value"] = self.mem[variable["name"]]["value"]
			variable["monitorData"] = self.mem[variable["name"]]["monitorData"]

		return projectData

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
		
			if os.path.isfile('listing.json') and os.path.isfile('project.json') and not self._stop_event.is_set():
			
				self.mem = {}
				self.rlo = {}

				with open('project.json') as f:
					self.projectdata = json.load(f)

				self.checksum = self.getProjectdataChecksum(self.projectdata)
					
				with open('listing.json', 'r') as file:
					listingdata = json.load(file)

				for var in self.projectdata["variables"]:
					self.mem[var["name"]] = var
					self.mem[var["name"]]["value"] = 0

				for setupentry in listingdata[0]['setuplisting']:
					setupfunc = setupentry["functionName"]
					#print(setupfunc + " " + str(setupentry["id"]))
					if setupfunc in globals():						
						f_ptr = globals()[setupfunc]
						f_ptr(setupentry, self.mem)
						#print(self.rlo)
						#print(self.mem)

				while not self._stop_event.is_set():
					time.sleep(0.1)
					#print("---------------------")

					for entry in listingdata[0]['listing']:

						if "memoryAddr" in entry and entry["memoryAddr"] != " " and entry["memoryAddr"] in self.mem:

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
							
						#print(self.mem)
						#print("--------------")
						#print(self.rlo)
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
			#print(post_data)
			programThread.forceVariables(post_data)
			#response_object['variablesdata'] = programThread.variablesdata
	response_object['statusdata'] = programThread.getStatus()
	return jsonify(response_object)

@app.route('/pullruntimedata', methods=['GET'])
@cross_origin(origin='*')
def pullRuntimeData():
	response_object = {}
	if request.method == 'GET':
		if programThread.isRunning():
			#response_object['variablesdata'] = programThread.getVariablesValuesInVariablesData(programThread.variablesdata)
			#response_object['projectdata'] = programThread.getNodesAndInputsValuesInProjectData(programThread.projectdata)
			response_object['project'] = programThread.pullRuntimeValuesToProjectData(programThread.projectdata)
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
			#print('checksum:', post_data["checksum"])
			#print(programThread.getProjectdataChecksum(programThread.projectdata))
			if post_data["checksum"] == programThread.getProjectdataChecksum(programThread.projectdata):
				with open('project.json', 'w') as f:
					f.write(json.dumps(post_data))
				response_object['checksum'] = 'ok';
				programThread.projectdata = post_data
				programThread.changed = True
				programThread.saveStatusToFile()
				response_object['statusdata'] = programThread.getStatus()
			else:
				response_object['checksum'] = 'bad';
	elif request.method == 'GET':
		response_object['project'] = programThread.projectdata
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


