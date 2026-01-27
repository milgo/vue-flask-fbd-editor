extends Node

var _setupListing
var _programListing

var _mem: Dictionary
var _rlo: Dictionary

var _running: bool

signal send_data(data:String)
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
		for commandJson in _programListing:
			var command: Dictionary = commandJson			
			call(command["functionName"], command)
	pass

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
	
#---------- DIN ----------	
func setup_DIN(_this: Dictionary):
	_mem[_this["memoryAddr"]] = 0

func before_DIN(_this: Dictionary):
	_mem[_this["id"]] = _mem[_this["memoryAddr"]]
	
func after_DIN(_this: Dictionary):
	_rlo[_this["id"]] = _mem[_this["id"]]
#---------- AND ----------
func before_AND(_data: Dictionary):
	_mem[_data["id"]] = 1
	
func after_AND_INPUT(_data: Dictionary):
	if(_rlo[_data["connNodeId"]] == 0):
		_mem[_data["id"]] = 0

func after_AND(_data: Dictionary):
	_rlo[_data["id"]] = _mem[_data["id"]]
