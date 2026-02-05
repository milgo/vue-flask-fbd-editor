extends Node

var _setupListing
var _programListing

var _mem: Dictionary
var _prev_mem : Dictionary
var _rlo: Dictionary
var _running: bool
var _FalseTrue = ["False", "True"]

signal send_data(data:String)
signal variable_value_changed(memAddr:String, oldval:String, newval:String)

var _send_data_timer = Timer.new()

func _ready() -> void:
	_send_data_timer.connect("timeout", _on_send_data_timer)
	_send_data_timer.wait_time = 0.1
	_running = false
	add_child(_send_data_timer)

func execute(json):
	if(json["reciver"] == "backend"):
		print(str("Logic command: ", json["command"]))
		
		if(json["command"] == "start"):
			_setupListing = json["data"]["setuplisting"]
			_programListing = json["data"]["listing"]
		
			print(str(_setupListing))
			print(str(_programListing))
			
			var started_json_info: Dictionary
			started_json_info["command"] = "started"
			started_json_info["reciver"] = "frontend"
			send_data.emit(JSON.stringify(started_json_info));			
		
			for setupJson in _setupListing:
				var setup: Dictionary = setupJson
				
				if setup.has("memoryAddr"):
					#if setup["memoryAddr"].begins_with("%"):
					var vdict:Dictionary
					vdict["value"] = 0
					_mem[setup["memoryAddr"]] = vdict
				
				var ndict:Dictionary
				ndict["value"] = 0
				_mem[setup["id"]] = ndict
					
				call(setup["functionName"], setup)				
			
			_running = true
			
		if(json["command"] == "monitorOn"):	
			_send_data_timer.start()
			
		if(json["command"] == "monitorOff"):	
			_send_data_timer.stop()
			var data_to_send : Dictionary
			data_to_send["command"] = "monitorOff"
			data_to_send["reciver"] = "frontend"
			var jsonStr = JSON.stringify(data_to_send)
			send_data.emit(jsonStr)	
				
		if(json["command"] == "stop"):
			_running = false
			_send_data_timer.stop()
			
			var stopped_json_info: Dictionary
			stopped_json_info["command"] = "stopped"
			stopped_json_info["reciver"] = "frontend"
			send_data.emit(JSON.stringify(stopped_json_info));			
			
		if(json["command"] == "forcevariables"):			
			for fvar in json["data"]:
				print(JSON.stringify(fvar))
				_mem[fvar["name"]]["forced"] = fvar["forced"]
				_mem[fvar["name"]]["forcedValue"] = fvar["forcedValue"]

func getVariableValue(memoryAddr:String):
	if _mem[memoryAddr].has("forced") and _mem[memoryAddr].has("forcedValue"):
		if _mem[memoryAddr]["forced"] == 1:
			return _mem[memoryAddr]["forcedValue"]
	return _mem[memoryAddr]["value"]

func _on_digital_state_changed(memAddr: String, state: int) -> void:
	_mem[memAddr]["value"] = state
	pass # Replace with function body.
	
func _process(_delta: float) -> void:
	if _running:	
		
		for key in _mem.keys():
			var k:String = key
			_prev_mem[k] = str(_mem[k]["value"])
			
		for commandJson in _programListing:
			var command: Dictionary = commandJson			
			call(command["functionName"], command)
		
		for key in _mem.keys():
			var newval: String
			var k:String = key
			newval = str(_mem[k]["value"])
			if newval != _prev_mem[k]:
				#print("compere: " + newval + "!=" + _prev_mem[k])
				variable_value_changed.emit(k, _prev_mem[k], newval)			
	

func _on_send_data_timer():
	var data_to_send : Dictionary
	data_to_send["command"] = "monitorOn"
	data_to_send["reciver"] = "frontend"
	data_to_send["rlo"] = _rlo
	data_to_send["mem"] = _mem	
	var jsonStr = JSON.stringify(data_to_send)
	send_data.emit(jsonStr)	
	
func _on_simulation_button_button_up() -> void:
	pass # Replace with function body.	
	
#---------- CONST ----------	
func setup_CONST(_data: Dictionary):
	_rlo[_data["id"]] = int(_data["memoryAddr"])
	
#---------- VAR ----------
func after_VAR(_data: Dictionary):
	_rlo[_data["id"]] = getVariableValue(_data["memoryAddr"])
	
#---------- TIME ----------
func setup_TIME(_data: Dictionary):
	var regex = RegEx.create_from_string("\\d{1,6}")
	var res = regex.search(_data["memoryAddr"])
	if res:
		_mem[_data["id"]]["value"] = res.get_string()
	
func after_TIME(_data: Dictionary):
	_rlo[_data["id"]] = _mem[_data["id"]]["value"] 
	
#---------- DIN -----------
func setup_DIN(_data: Dictionary):
	pass

func before_DIN(_data: Dictionary):
	_mem[_data["id"]]["value"]  = getVariableValue(_data["memoryAddr"])
	
func after_DIN(_data: Dictionary):
	_rlo[_data["id"]] = _mem[_data["id"]]["value"] 
	_mem[_data["memoryAddr"]]["monitorData"] = _FalseTrue[getVariableValue(_data["memoryAddr"])]
	
#---------- AND ----------
func before_AND(_data: Dictionary):
	_mem[_data["id"]]["value"]  = 1
	
func after_AND_INPUT(_data: Dictionary):
	if(_rlo[_data["connNodeId"]] == 0):
		_mem[_data["id"]]["value"] = 0

func after_AND(_data: Dictionary):
	_rlo[_data["id"]] = _mem[_data["id"]]["value"] 
	
#---------- OR ----------
func before_OR(_data: Dictionary):
	_mem[_data["id"]]["value"]  = 0
	
func after_OR_INPUT(_data: Dictionary):
	if(_rlo[_data["connNodeId"]] == 1):
		_mem[_data["id"]]["value"]  = 1

func after_OR(_data: Dictionary):
	_rlo[_data["id"]] = _mem[_data["id"]]["value"] 
	
#---------- NOT ----------
func before_NOT(_data: Dictionary):
	_mem[_data["id"]]["value"]  = 0
	
func after_NOT_INPUT(_data: Dictionary):
	if _rlo[_data["connNodeId"]] == 1:
		_mem[_data["id"]]["value"]  = 0
	else:
		_mem[_data["id"]]["value"]  = 1

func after_NOT(_data: Dictionary):
	_rlo[_data["id"]] = _mem[_data["id"]]["value"] 
	
#---------- ASSIGN ----------
func before_ASSIGN(_data: Dictionary):
	_mem[_data["id"]]["value"]  = 0
	
func after_ASSIGN_INPUT(_data: Dictionary):
	_mem[_data["id"]]["value"]  = _rlo[_data["connNodeId"]] 

func after_ASSIGN(_data: Dictionary):
	_rlo[_data["id"]] = _mem[_data["id"]]["value"]
	_mem[_data["memoryAddr"]]["value"]  = _mem[_data["id"]]["value"] 
	_mem[_data["memoryAddr"]]["monitorData"] = _FalseTrue[_mem[_data["memoryAddr"]]["value"]]
	
#---------- SET ----------
func before_SET(_data: Dictionary):
	_mem[_data["id"]]["value"]  = 0
	
func after_SET_INPUT(_data: Dictionary):
	if _rlo[_data["connNodeId"]] == 1:
		_mem[_data["memoryAddr"]]["value"]  = 1

func after_SET(_data: Dictionary):
	_rlo[_data["id"]] = getVariableValue(_data["memoryAddr"])
	_mem[_data["memoryAddr"]]["monitorData"] = _FalseTrue[_mem[_data["memoryAddr"]]["value"]]
	
#---------- RESET ----------
func before_RESET(_data: Dictionary):
	_mem[_data["id"]] = 0
	
func after_RESET_INPUT(_data: Dictionary):
	if _rlo[_data["connNodeId"]] == 1:
		_mem[_data["memoryAddr"]]["value"]  = 0

func after_RESET(_data: Dictionary):
	_rlo[_data["id"]] = getVariableValue(_data["memoryAddr"])
	_mem[_data["memoryAddr"]]["monitorData"] = _FalseTrue[_mem[_data["memoryAddr"]]["value"]]
#---------- SET/RESET ----------
func before_SR(_data: Dictionary):
	_mem[_data["id"]] = 0
	
func after_SR_INPUT(_data: Dictionary):
	if _data["inputName"] == "S":
		if _rlo[_data["connNodeId"]] == 1:
			_mem[_data["memoryAddr"]]["value"]  = 1
	if _data["inputName"] == "R":
		if _rlo[_data["connNodeId"]] == 1:
			_mem[_data["memoryAddr"]]["value"]  = 0

func after_SR(_data: Dictionary):
	_rlo[_data["id"]] = getVariableValue(_data["memoryAddr"]) 
	_mem[_data["memoryAddr"]]["monitorData"] = _FalseTrue[_mem[_data["memoryAddr"]]["value"]]
	
#---------- RESET/SET ----------
func before_RS(_data: Dictionary):
	_mem[_data["id"]]["value"]  = 0
	
func after_RS_INPUT(_data: Dictionary):
	if _data["inputName"] == "R":
		if _rlo[_data["connNodeId"]] == 1:
			_mem[_data["memoryAddr"]]["value"]  = 0
			
	if _data["inputName"] == "S":
		if _rlo[_data["connNodeId"]] == 1:
			_mem[_data["memoryAddr"]]["value"]  = 1

func after_RS(_data: Dictionary):
	_rlo[_data["id"]] = getVariableValue(_data["memoryAddr"])
	_mem[_data["memoryAddr"]]["monitorData"] = _FalseTrue[_mem[_data["memoryAddr"]]["value"]]
#---------- FP ----------
func before_FP(_data: Dictionary):
	_mem[_data["id"]]["value"]  = 0
	
func after_FP_INPUT(_data: Dictionary):
	if _rlo[_data["connNodeId"]] == 1 and _mem[_data["memoryAddr"]]["value"]  == 0:
		_mem[_data["id"]]["value"]  = 1
	_mem[_data["memoryAddr"]]["value"]  = _rlo[_data["connNodeId"]]

func after_FP(_data: Dictionary):
	_rlo[_data["id"]] = _mem[_data["id"]]["value"] 
	_mem[_data["memoryAddr"]]["monitorData"] = _FalseTrue[_mem[_data["memoryAddr"]]["value"]]
	
#---------- FN ----------
func before_FN(_data: Dictionary):
	_mem[_data["id"]] = 0
	
func after_FN_INPUT(_data: Dictionary):
	if _rlo[_data["connNodeId"]] == 0 and _mem[_data["memoryAddr"]]["value"]  == 1:
		_mem[_data["id"]]["value"]  = 1
	_mem[_data["memoryAddr"]]["value"]  = _rlo[_data["connNodeId"]]

func after_FN(_data: Dictionary):
	_rlo[_data["id"]] = _mem[_data["id"]]["value"] 
	_mem[_data["memoryAddr"]]["monitorData"] = _FalseTrue[_mem[_data["memoryAddr"]]["value"]]
	
#---------- MOVE ----------
func before_MOVE(_data: Dictionary):
	_mem[_data["id"]]["value"]  = 0
	
func after_MOVE_INPUT(_data: Dictionary):
	_mem[_data["memoryAddr"]]["value"] = _rlo[_data["connNodeId"]]

func after_MOVE(_data: Dictionary):
	_rlo[_data["id"]] = getVariableValue(_data["memoryAddr"])
	_mem[_data["memoryAddr"]]["monitorData"] = getVariableValue(_data["memoryAddr"])
	
#---------- SP ----------
func setup_SP(_data: Dictionary):
	_mem[_data["memoryAddr"]]["started"]  = 0
	_mem[_data["memoryAddr"]]["startTime"]  = 0
	_mem[_data["memoryAddr"]]["elapsedTime"]  = 0
	_mem[_data["memoryAddr"]]["stopped"]  = 0
	
func before_SP(_data: Dictionary):
	if _mem[_data["memoryAddr"]]["started"] == 1:
		if _mem[_data["memoryAddr"]]["stopped"] == 0:
			_mem[_data["memoryAddr"]]["elapsedTime"] = Time.get_ticks_msec() - _mem[_data["memoryAddr"]]["startTime"]
			_mem[_data["memoryAddr"]]["value"] = _mem[_data["memoryAddr"]]["elapsedTime"]
		if _mem[_data["memoryAddr"]]["elapsedTime"] < _mem[_data["memoryAddr"]]["duration"]:
			_mem[_data["memoryAddr"]]["value"] = 1
		else:
			_mem[_data["memoryAddr"]]["value"] = 0
			_mem[_data["memoryAddr"]]["stopped"] = 1
			_mem[_data["memoryAddr"]]["monitorData"] = 0

func after_SP_INPUT(_data: Dictionary):
	if _data["inputName"] == "S":
		if _rlo[_data["connNodeId"]] == 1 and _mem[_data["memoryAddr"]]["started"] == 0:
			_mem[_data["memoryAddr"]]["started"] = 1
			_mem[_data["memoryAddr"]]["startTime"] = Time.get_ticks_msec()
		if _rlo[_data["connNodeId"]] == 0:
			_mem[_data["memoryAddr"]]["started"] = 0
			_mem[_data["memoryAddr"]]["stopped"] = 0
			_mem[_data["memoryAddr"]]["value"] = 0
	
	if _data["inputName"] == "T":
		_mem[_data["memoryAddr"]]["duration"] = int(_rlo[_data["connNodeId"]])

func after_SP(_data: Dictionary):
	_rlo[_data["id"]] = getVariableValue(_data["memoryAddr"])
	_mem[_data["memoryAddr"]]["monitorData"] = _mem[_data["memoryAddr"]]["elapsedTime"]

#---------- SE ----------
func setup_SE(_data: Dictionary):
	_mem[_data["memoryAddr"]]["started"]  = 0
	_mem[_data["memoryAddr"]]["startTime"]  = 0
	_mem[_data["memoryAddr"]]["elapsedTime"]  = 0
	_mem[_data["memoryAddr"]]["stopped"]  = 0
	
func before_SE(_data: Dictionary):
	
	if _mem[_data["memoryAddr"]]["started"] == 1 and _mem[_data["memoryAddr"]]["stopped"] == 1 and _mem[_data["memoryAddr"]]["elapsedTime"] > _mem[_data["memoryAddr"]]["duration"]:
		_mem[_data["memoryAddr"]]["started"]  = 0
		_mem[_data["memoryAddr"]]["startTime"]  = 0
		_mem[_data["memoryAddr"]]["elapsedTime"]  = 0
		_mem[_data["memoryAddr"]]["stopped"]  = 0
	
	if _mem[_data["memoryAddr"]]["started"] == 1:
		if _mem[_data["memoryAddr"]]["stopped"] == 0:
			_mem[_data["memoryAddr"]]["elapsedTime"] = Time.get_ticks_msec() - _mem[_data["memoryAddr"]]["startTime"]
			_mem[_data["memoryAddr"]]["value"] = _mem[_data["memoryAddr"]]["elapsedTime"]
		if _mem[_data["memoryAddr"]]["elapsedTime"] < _mem[_data["memoryAddr"]]["duration"]:
			_mem[_data["memoryAddr"]]["value"] = 1
		else:
			_mem[_data["memoryAddr"]]["value"] = 0
			_mem[_data["memoryAddr"]]["stopped"] = 1
			_mem[_data["memoryAddr"]]["monitorData"] = 0

func after_SE_INPUT(_data: Dictionary):
	if _data["inputName"] == "S":
		if _rlo[_data["connNodeId"]] == 1 and _mem[_data["memoryAddr"]]["started"] == 0 and _mem[_data["memoryAddr"]]["stopped"] == 0:
			_mem[_data["memoryAddr"]]["started"] = 1
			_mem[_data["memoryAddr"]]["startTime"] = Time.get_ticks_msec()
		if _rlo[_data["connNodeId"]] == 0 and _mem[_data["memoryAddr"]]["started"] == 0 and _mem[_data["memoryAddr"]]["stopped"] == 1:
			_mem[_data["memoryAddr"]]["stopped"] = 0
			_mem[_data["memoryAddr"]]["value"] = 0
	
	if _data["inputName"] == "T":
		_mem[_data["memoryAddr"]]["duration"] = int(_rlo[_data["connNodeId"]])

func after_SE(_data: Dictionary):
	_rlo[_data["id"]] = getVariableValue(_data["memoryAddr"])
	_mem[_data["memoryAddr"]]["monitorData"] = _mem[_data["memoryAddr"]]["elapsedTime"]

#---------- SD ----------
func setup_SD(_data: Dictionary):
	_mem[_data["memoryAddr"]]["started"]  = 0
	_mem[_data["memoryAddr"]]["startTime"]  = 0
	_mem[_data["memoryAddr"]]["elapsedTime"]  = 0
	_mem[_data["memoryAddr"]]["stopped"]  = 0
	
func before_SD(_data: Dictionary):
	if _mem[_data["memoryAddr"]]["started"] == 1:
		if _mem[_data["memoryAddr"]]["stopped"] == 0:
			_mem[_data["memoryAddr"]]["elapsedTime"] = Time.get_ticks_msec() - _mem[_data["memoryAddr"]]["startTime"]
			_mem[_data["memoryAddr"]]["value"] = _mem[_data["memoryAddr"]]["elapsedTime"]
		if _mem[_data["memoryAddr"]]["elapsedTime"] < _mem[_data["memoryAddr"]]["duration"]:
			_mem[_data["memoryAddr"]]["value"] = 0
		else:
			_mem[_data["memoryAddr"]]["value"] = 1
			_mem[_data["memoryAddr"]]["stopped"] = 1
			_mem[_data["memoryAddr"]]["monitorData"] = 0

func after_SD_INPUT(_data: Dictionary):
	if _data["inputName"] == "S":
		if _rlo[_data["connNodeId"]] == 1 and _mem[_data["memoryAddr"]]["started"] == 0:
			_mem[_data["memoryAddr"]]["started"] = 1
			_mem[_data["memoryAddr"]]["startTime"] = Time.get_ticks_msec()
		if _rlo[_data["connNodeId"]] == 0:
			_mem[_data["memoryAddr"]]["started"] = 0
			_mem[_data["memoryAddr"]]["stopped"] = 0
			_mem[_data["memoryAddr"]]["value"] = 0
	
	if _data["inputName"] == "T":
		_mem[_data["memoryAddr"]]["duration"] = int(_rlo[_data["connNodeId"]])

func after_SD(_data: Dictionary):
	_rlo[_data["id"]] = getVariableValue(_data["memoryAddr"])
	_mem[_data["memoryAddr"]]["monitorData"] = _mem[_data["memoryAddr"]]["elapsedTime"]

#---------- SS ----------
func setup_SS(_data: Dictionary):
	_mem[_data["memoryAddr"]]["started"]  = 0
	_mem[_data["memoryAddr"]]["startTime"]  = 0
	_mem[_data["memoryAddr"]]["elapsedTime"]  = 0
	_mem[_data["memoryAddr"]]["stopped"]  = 0
	
func before_SS(_data: Dictionary):
	if _mem[_data["memoryAddr"]]["started"] == 1:
		if _mem[_data["memoryAddr"]]["stopped"] == 0:
			_mem[_data["memoryAddr"]]["elapsedTime"] = Time.get_ticks_msec() - _mem[_data["memoryAddr"]]["startTime"]
			_mem[_data["memoryAddr"]]["value"] = _mem[_data["memoryAddr"]]["elapsedTime"]
		if _mem[_data["memoryAddr"]]["elapsedTime"] < _mem[_data["memoryAddr"]]["duration"]:
			_mem[_data["memoryAddr"]]["value"] = 0
		else:
			_mem[_data["memoryAddr"]]["value"] = 1
			_mem[_data["memoryAddr"]]["stopped"] = 1
			_mem[_data["memoryAddr"]]["monitorData"] = 0

func after_SS_INPUT(_data: Dictionary):
	if _data["inputName"] == "S":
		if _rlo[_data["connNodeId"]] == 1 and _mem[_data["memoryAddr"]]["started"] == 0:
			_mem[_data["memoryAddr"]]["started"] = 1
			_mem[_data["memoryAddr"]]["startTime"] = Time.get_ticks_msec()
		
	if _data["inputName"] == "R":		
		if _rlo[_data["connNodeId"]] == 1:
			_mem[_data["memoryAddr"]]["started"] = 0
			_mem[_data["memoryAddr"]]["stopped"] = 0
			_mem[_data["memoryAddr"]]["value"] = 0
	
	if _data["inputName"] == "T":
		_mem[_data["memoryAddr"]]["duration"] = int(_rlo[_data["connNodeId"]])

func after_SS(_data: Dictionary):
	_rlo[_data["id"]] = getVariableValue(_data["memoryAddr"])
	_mem[_data["memoryAddr"]]["monitorData"] = _mem[_data["memoryAddr"]]["elapsedTime"]

#---------- SF ----------
func setup_SF(_data: Dictionary):
	_mem[_data["memoryAddr"]]["started"]  = 0
	_mem[_data["memoryAddr"]]["startTime"]  = 0
	_mem[_data["memoryAddr"]]["elapsedTime"]  = 0
	_mem[_data["memoryAddr"]]["stopped"]  = 0
	
func before_SF(_data: Dictionary):
	if _mem[_data["memoryAddr"]]["started"] == 1:
		if _mem[_data["memoryAddr"]]["stopped"] == 0:
			_mem[_data["memoryAddr"]]["elapsedTime"] = Time.get_ticks_msec() - _mem[_data["memoryAddr"]]["startTime"]
			_mem[_data["memoryAddr"]]["value"] = _mem[_data["memoryAddr"]]["elapsedTime"]
		if _mem[_data["memoryAddr"]]["elapsedTime"] < _mem[_data["memoryAddr"]]["duration"]:
			_mem[_data["memoryAddr"]]["value"] = 0
		else:
			_mem[_data["memoryAddr"]]["value"] = 1
			_mem[_data["memoryAddr"]]["started"] = 0
			_mem[_data["memoryAddr"]]["stopped"] = 1
			_mem[_data["memoryAddr"]]["monitorData"] = 0

func after_SF_INPUT(_data: Dictionary):
	if _data["inputName"] == "S":
		if _rlo[_data["connNodeId"]] == 0 and _mem[_data["memoryAddr"]]["started"] == 0 and _mem[_data["memoryAddr"]]["stopped"] == 0:
			_mem[_data["memoryAddr"]]["started"] = 1
			_mem[_data["memoryAddr"]]["startTime"] = Time.get_ticks_msec()
		if _rlo[_data["connNodeId"]] == 1 and _mem[_data["memoryAddr"]]["started"] == 0 and _mem[_data["memoryAddr"]]["stopped"] == 1:
			_mem[_data["memoryAddr"]]["started"] = 0
			_mem[_data["memoryAddr"]]["stopped"] = 0
			_mem[_data["memoryAddr"]]["value"] = 0
	
	if _data["inputName"] == "T":
		_mem[_data["memoryAddr"]]["duration"] = int(_rlo[_data["connNodeId"]])

func after_SF(_data: Dictionary):
	_rlo[_data["id"]] = 0 
	if _mem[_data["memoryAddr"]]["value"] == 0:
		_rlo[_data["id"]] = 1
	_mem[_data["memoryAddr"]]["monitorData"] = _mem[_data["memoryAddr"]]["elapsedTime"]

#---------- CU ----------
func setup_CU(_data: Dictionary):
	_mem[_data["memoryAddr"]]["edge"] = 0
	
func after_CU_INPUT(_data: Dictionary):
	if _data["inputName"] == "INC":
		if _rlo[_data["connNodeId"]] == 1:
			if _mem[_data["memoryAddr"]]["edge"] == 0:				
				_mem[_data["memoryAddr"]]["value"] = _mem[_data["memoryAddr"]]["value"] + 1
				_mem[_data["memoryAddr"]]["monitorData"] = getVariableValue(_data["memoryAddr"])
				_mem[_data["memoryAddr"]]["edge"] = 1
		else:
			_mem[_data["memoryAddr"]]["edge"] = 0
				
	if _data["inputName"] == "R":
		if _rlo[_data["connNodeId"]] == 1:
			_mem[_data["memoryAddr"]]["value"] = 0
			_mem[_data["memoryAddr"]]["monitorData"] = 0

func after_CU(_data: Dictionary):
	_rlo[_data["id"]] = getVariableValue(_data["memoryAddr"])
	
#---------- CD ----------
func setup_CD(_data: Dictionary):
	_mem[_data["memoryAddr"]]["edge"] = 0
	
func after_CD_INPUT(_data: Dictionary):
	if _data["inputName"] == "DEC":
		if _rlo[_data["connNodeId"]] == 1:
			if _mem[_data["memoryAddr"]]["edge"] == 0:				
				_mem[_data["memoryAddr"]]["value"] = _mem[_data["memoryAddr"]]["value"] - 1
				_mem[_data["memoryAddr"]]["monitorData"] = getVariableValue(_data["memoryAddr"])
				_mem[_data["memoryAddr"]]["edge"] = 1
		else:
			_mem[_data["memoryAddr"]]["edge"] = 0
				
	if _data["inputName"] == "R":
		if _rlo[_data["connNodeId"]] == 1:
			_mem[_data["memoryAddr"]]["value"] = 0
			_mem[_data["memoryAddr"]]["monitorData"] = 0
			
func after_CD(_data: Dictionary):
	_rlo[_data["id"]] = getVariableValue(_data["memoryAddr"])
	
#---------- EQ ----------
func setup_EQ(_data: Dictionary):
	_mem[_data["id"]]["valueA"] = 0
	_mem[_data["id"]]["valueB"] = 0

func after_EQ_INPUT(_data: Dictionary):
	if _data["inputName"] == "IN1":
		_mem[_data["id"]]["valueA"] = _rlo[_data["connNodeId"]]

	if _data["inputName"] == "IN2":
		_mem[_data["id"]]["valueB"] = _rlo[_data["connNodeId"]]

func after_EQ(_data: Dictionary):
	_rlo[_data["id"]] = 0
	if _mem[_data["id"]]["valueA"] == _mem[_data["id"]]["valueB"]:
		_rlo[_data["id"]] = 1

#---------- GT ----------
func setup_GT(_data: Dictionary):
	_mem[_data["id"]]["valueA"] = 0
	_mem[_data["id"]]["valueB"] = 0

func after_GT_INPUT(_data: Dictionary):
	if _data["inputName"] == "IN1":
		_mem[_data["id"]]["valueA"] = _rlo[_data["connNodeId"]]

	if _data["inputName"] == "IN2":
		_mem[_data["id"]]["valueB"] = _rlo[_data["connNodeId"]]

func after_GT(_data: Dictionary):
	_rlo[_data["id"]] = 0
	if _mem[_data["id"]]["valueA"] > _mem[_data["id"]]["valueB"]:
		_rlo[_data["id"]] = 1

#---------- LT ----------
func setup_LT(_data: Dictionary):
	_mem[_data["id"]]["valueA"] = 0
	_mem[_data["id"]]["valueB"] = 0

func after_LT_INPUT(_data: Dictionary):
	if _data["inputName"] == "IN1":
		_mem[_data["id"]]["valueA"] = _rlo[_data["connNodeId"]]

	if _data["inputName"] == "IN2":
		_mem[_data["id"]]["valueB"] = _rlo[_data["connNodeId"]]

func after_LT(_data: Dictionary):
	_rlo[_data["id"]] = 0
	if _mem[_data["id"]]["valueA"] < _mem[_data["id"]]["valueB"]:
		_rlo[_data["id"]] = 1
		
#---------- GE ----------
func setup_GE(_data: Dictionary):
	_mem[_data["id"]]["valueA"] = 0
	_mem[_data["id"]]["valueB"] = 0

func after_GE_INPUT(_data: Dictionary):
	if _data["inputName"] == "IN1":
		_mem[_data["id"]]["valueA"] = _rlo[_data["connNodeId"]]

	if _data["inputName"] == "IN2":
		_mem[_data["id"]]["valueB"] = _rlo[_data["connNodeId"]]

func after_GE(_data: Dictionary):
	_rlo[_data["id"]] = 0
	if _mem[_data["id"]]["valueA"] >= _mem[_data["id"]]["valueB"]:
		_rlo[_data["id"]] = 1
		
#---------- LE ----------
func setup_LE(_data: Dictionary):
	_mem[_data["id"]]["valueA"] = 0
	_mem[_data["id"]]["valueB"] = 0

func after_LE_INPUT(_data: Dictionary):
	if _data["inputName"] == "IN1":
		_mem[_data["id"]]["valueA"] = _rlo[_data["connNodeId"]]

	if _data["inputName"] == "IN2":
		_mem[_data["id"]]["valueB"] = _rlo[_data["connNodeId"]]

func after_LE(_data: Dictionary):
	_rlo[_data["id"]] = 0
	if _mem[_data["id"]]["valueA"] <= _mem[_data["id"]]["valueB"]:
		_rlo[_data["id"]] = 1
		
#---------- ADD ----------
func setup_ADD(_data: Dictionary):
	_mem[_data["id"]]["value"] = 0 
	
func after_ADD_INPUT(_data: Dictionary):
	_mem[_data["id"]]["value"] = _mem[_data["id"]]["value"] + _rlo[_data["connNodeId"]]

func after_ADD(_data: Dictionary):
	_rlo[_data["id"]] = _mem[_data["id"]]["value"]
	_mem[_data["id"]]["value"] = 0

#---------- SUB ----------
func setup_SUB(_data: Dictionary):
	_mem[_data["id"]]["value"] = 0 
	
func after_SUB_INPUT(_data: Dictionary):
	if _mem[_data["id"]]["value"] == 0:
		_mem[_data["id"]]["value"] = _rlo[_data["connNodeId"]]
	else:
		_mem[_data["id"]]["value"] = _mem[_data["id"]]["value"] - _rlo[_data["connNodeId"]]

func after_SUB(_data: Dictionary):
	_rlo[_data["id"]] = _mem[_data["id"]]["value"]
	_mem[_data["id"]]["value"] = 0

#---------- MUL ----------
func setup_MUL(_data: Dictionary):
	_mem[_data["id"]]["value"] = 1 

func before_MUL(_data: Dictionary):
	_mem[_data["id"]]["value"] = 1 	

func after_MUL_INPUT(_data: Dictionary):
	_mem[_data["id"]]["value"] = _mem[_data["id"]]["value"] * _rlo[_data["connNodeId"]]

func after_MUL(_data: Dictionary):
	_rlo[_data["id"]] = _mem[_data["id"]]["value"]
	_mem[_data["id"]]["value"] = 0
	
#---------- DIV ----------
func setup_DIV(_data: Dictionary):
	_mem[_data["id"]]["value"] = 0 
	
func after_DIV_INPUT(_data: Dictionary):
	if _mem[_data["id"]]["value"] == 0:
		_mem[_data["id"]]["value"] = _rlo[_data["connNodeId"]]
	else:
		_mem[_data["id"]]["value"] = _mem[_data["id"]]["value"] / _rlo[_data["connNodeId"]]

func after_DIV(_data: Dictionary):
	_rlo[_data["id"]] = _mem[_data["id"]]["value"]
	_mem[_data["id"]]["value"] = 0
