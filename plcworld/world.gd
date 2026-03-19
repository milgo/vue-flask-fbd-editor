extends Node3D

static var game_count = 0 
@onready var pullDataTimer: Timer = $PullDataTimer

@onready var creator: Node3D = get_node("Creator")
@onready var ball = preload("res://ball.tscn")
#@onready var label: Label = get_node("/root/World/HUD/Label")
@onready var messageCallback: JavaScriptObject
@onready var logic = $Logic
@onready var goingUpInd = $HUD/VBoxContainer/HBoxContainer/VBoxContainer2/GoingUp
@onready var goingDownInd = $HUD/VBoxContainer/HBoxContainer/VBoxContainer2/GoingDown
var window: JavaScriptObject 

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	
	$HUD/MemDesc.visible = false
	window = JavaScriptBridge.get_interface("window")
	messageCallback = JavaScriptBridge.create_callback(_on_message_received)
	pullDataTimer.timeout.connect(_on_timeout)
	
	if window == null:
		return

	window.parent.addEventListener("message", messageCallback)	
	#use window.parent when game is running in iframe
	#window.parent.postMessage("done", "*")
		

	#$HTTPRequest.request_completed.connect(_on_request_completed)
	pass # Replace with function body.
	
func _on_message_received(args):
	var json = JSON.parse_string(args[0].data)
	#print(args[0].data)	
	logic.execute(json)
	pass
	
func _on_logic_send_data(data: String) -> void:
	window.parent.postMessage(data, "*")
	pass # Replace with function body.


#func _on_request_completed(_result, _response_code, _headers, body):
#	var json = JSON.parse_string(body.get_string_from_utf8())
#	print(json)
	
	#var data_dict = json
	#for key in data_dict:
	#	print(data_dict[key])
	
	#print(json["project"]["checksum"])
	pass

func _on_timeout() -> void:
	pass

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float) -> void:
	pass
	
func _post_request() -> void:
	#var json = JSON.stringify(data_to_send)
	#var headers = ["Content-Type: application/json"]
	#$HTTPRequest.request(url, headers, HTTPClient.METHOD_POST, json)
	pass

func _on_logic_variable_value_changed(memAddr: String, oldval: String, newval: String) -> void:
	var newvalf = float(newval)
	#print("var " + memAddr + " changed from " + oldval + " to " + newval)
	#if memAddr == "%o1" and newval == "1":
#		var new_ball = ball.instantiate()
		#new_ball.set_position(creator.get_position())
		#add_child(new_ball)
	if memAddr == goingUpInd.get_meta("DO"):
		if newvalf == 1.0:
			goingUpInd.texture = load("res://elevator-project/going_up_green.png")
		else:
			goingUpInd.texture = load("res://elevator-project/going_up_gray.png")
	
	if memAddr == goingDownInd.get_meta("DO"):
		if newvalf == 1.0:
			goingDownInd.texture = load("res://elevator-project/going_down_green.png")
		else:
			goingDownInd.texture = load("res://elevator-project/going_down_gray.png")
	

func _on_level_limit_switch_area_entered(area: Area3D) -> void:
	if area.get_meta_list().has("DI"):
		logic.set_var_value(area.get_meta("DI"), 1)


func _on_level_limit_switch_area_exited(area: Area3D) -> void:
	if area.get_meta_list().has("DI"):
		logic.set_var_value(area.get_meta("DI"), 0)


func _on_button_down(extra_arg_0: String) -> void:
	logic.set_var_value(extra_arg_0, 1)
	pass # Replace with function body.


func _on_button_up(extra_arg_0: String) -> void:
	logic.set_var_value(extra_arg_0, 0)
	pass # Replace with function body.


func _on_info_button_button_down() -> void:
	$HUD/MemDesc.visible = true
	pass # Replace with function body.


func _on_info_button_button_up() -> void:
	$HUD/MemDesc.visible = false
	pass # Replace with function body.
