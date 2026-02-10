extends Node3D

static var game_count = 0 
@onready var pullDataTimer: Timer = $PullDataTimer

@onready var creator: Node3D = get_node("Creator")
@onready var ball = preload("res://ball.tscn")
@onready var label: Label = get_node("/root/World/HUD/Label")
@onready var messageCallback: JavaScriptObject
@onready var logic = $Logic

var window: JavaScriptObject 

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	
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
	print("var " + memAddr + " changed from " + oldval + " to " + newval)
	if memAddr == "%o1" and newval == "1":
		var new_ball = ball.instantiate()
		new_ball.set_position(creator.get_position())
		add_child(new_ball)
