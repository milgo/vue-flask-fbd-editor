extends Node

var _setupListing
var _programListing

var _mem: Dictionary
var _prev_mem : Dictionary
var _rlo: Dictionary

var _running: bool

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
					if setup["memoryAddr"].begins_with("%"):
						var vdict:Dictionary
						vdict["value"] = 0
						_mem[setup["memoryAddr"]] = vdict
				
				var ndict:Dictionary
				ndict["value"] = 0
				_mem[setup["id"]] = ndict
					
				call(setup["functionName"], setup)				
			
			_running = true
			_send_data_timer.start()
			
		if(json["command"] == "stop"):
			_running = false
			_send_data_timer.stop()
			
			var stopped_json_info: Dictionary
			stopped_json_info["command"] = "stopped"
			stopped_json_info["reciver"] = "frontend"
			send_data.emit(JSON.stringify(stopped_json_info));			

func _on_digital_state_changed(memAddr: String, state: int) -> void:
	_mem[memAddr] = state
	pass # Replace with function body.
	
func _process(_delta: float) -> void:
	if _running:	
		
		for key in _mem.keys():
			var k:String = key
			_prev_mem[k] = _mem[k]
			
		for commandJson in _programListing:
			var command: Dictionary = commandJson			
			call(command["functionName"], command)
			
		for key in _mem.keys():
			var k:String = key
			if str(_mem[k]) != str(_prev_mem[k]):
				variable_value_changed.emit(k, str(_prev_mem[key]), str(_mem[key]))			
	

func _on_send_data_timer():
	var data_to_send : Dictionary
	data_to_send["command"] = "monitor"
	data_to_send["reciver"] = "frontend"
	data_to_send["rlo"] = _rlo
	data_to_send["mem"] = _mem	
	var jsonStr = JSON.stringify(data_to_send)
	send_data.emit(jsonStr)	
	
func _on_simulation_button_button_up() -> void:
	pass # Replace with function body.	
	
#---------- CONST ----------	
func after_CONST(_data: Dictionary):
	_rlo[_data["id"]] = int(_data["memoryAddr"]["value"] )
	
#---------- DIN -----------
func setup_DIN(_data: Dictionary):
	pass

func before_DIN(_data: Dictionary):
	_mem[_data["id"]]["value"]  = _mem[_data["memoryAddr"]]["value"] 
	
func after_DIN(_data: Dictionary):
	_rlo[_data["id"]] = _mem[_data["id"]]["value"] 
	
#---------- AND ----------
func before_AND(_data: Dictionary):
	_mem[_data["id"]]["value"]  = 1
	
func after_AND_INPUT(_data: Dictionary):
	if(_rlo[_data["connNodeId"]] == 0):
		_mem[_data["id"]]["value"]  = 0

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
		_mem[_data["id"]]["value"]  = 0

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

#---------- SET ----------
func before_SET(_data: Dictionary):
	_mem[_data["id"]]["value"]  = 0
	
func after_SET_INPUT(_data: Dictionary):
	if _rlo[_data["connNodeId"]] == 1:
		_mem[_data["memoryAddr"]]["value"]  = 1

func after_SET(_data: Dictionary):
	_rlo[_data["id"]] = _mem[_data["memoryAddr"]]["value"] 

#---------- RESET ----------
func before_RESET(_data: Dictionary):
	_mem[_data["id"]] = 0
	
func after_RESET_INPUT(_data: Dictionary):
	if _rlo[_data["connNodeId"]] == 1:
		_mem[_data["memoryAddr"]]["value"]  = 0

func after_RESET(_data: Dictionary):
	_rlo[_data["id"]] = _mem[_data["memoryAddr"]]["value"] 

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
	_rlo[_data["id"]] = _mem[_data["memoryAddr"]]["value"] 

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
	_rlo[_data["id"]] = _mem[_data["memoryAddr"]]["value"] 

#---------- FP ----------
func before_FP(_data: Dictionary):
	_mem[_data["id"]]["value"]  = 0
	
func after_FP_INPUT(_data: Dictionary):
	if _rlo[_data["connNodeId"]] == 1 and _mem[_data["memoryAddr"]]["value"]  == 0:
		_mem[_data["id"]]["value"]  = 1
	_mem[_data["memoryAddr"]]["value"]  = _rlo[_data["connNodeId"]]

func after_FP(_data: Dictionary):
	_rlo[_data["id"]] = _mem[_data["id"]]["value"] 

#---------- FN ----------
func before_FN(_data: Dictionary):
	_mem[_data["id"]] = 0
	
func after_FN_INPUT(_data: Dictionary):
	if _rlo[_data["connNodeId"]] == 0 and _mem[_data["memoryAddr"]]["value"]  == 1:
		_mem[_data["id"]]["value"]  = 1
	_mem[_data["memoryAddr"]]["value"]  = _rlo[_data["connNodeId"]]

func after_FN(_data: Dictionary):
	_rlo[_data["id"]] = _mem[_data["id"]]["value"] 

#---------- MOVE ----------
func before_MOVE(_data: Dictionary):
	_mem[_data["id"]]["value"]  = 0
	
func after_MOVE_INPUT(_data: Dictionary):
	_mem[_data["memoryAddr"]]["value"] = _rlo[_data["connNodeId"]]

func after_MOVE(_data: Dictionary):
	_rlo[_data["id"]] = _mem[_data["memoryAddr"]]["value"] 
	
