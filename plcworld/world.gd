extends Node3D

static var game_count = 0 
@onready var pullDataTimer: Timer = $PullDataTimer

@onready var creator: Node3D = get_node("Creator")
@onready var ball = preload("res://ball.tscn")
@onready var label: Label = get_node("/root/World/HUD/Label")
@onready var simButton: Button = get_node("/root/World/HUD/SimulationButton")
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
	print(args[0].data)	
	logic.execute(JSON.parse_string(args[0].data))
	pass
	
func _on_logic_send_data(data: String) -> void:
	window.parent.postMessage(data, "*")
	pass # Replace with function body.


func _on_request_completed(_result, _response_code, _headers, body):
	var json = JSON.parse_string(body.get_string_from_utf8())
	print(json)
	
	#var data_dict = json
	#for key in data_dict:
	#	print(data_dict[key])
	
	#print(json["project"]["checksum"])
	pass

func _on_timeout() -> void:
	print("tick")
	var new_ball = ball.instantiate()
	new_ball.set_position(creator.get_position())
	add_child(new_ball)
	
	#$HTTPRequest.request("https://vue-flask-fbd-editor-6aim.onrender.com/project",)

	pass

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float) -> void:
	pass
	
func _post_request() -> void:
	#var json = JSON.stringify(data_to_send)
	#var headers = ["Content-Type: application/json"]
	#$HTTPRequest.request(url, headers, HTTPClient.METHOD_POST, json)
	pass

func _on_show_description(desc: Variant) -> void:
	label.text = desc	
	pass # Replace with function body.


func _on_limit_switch_state_changed(memAddr: Variant, state: Variant) -> void:
	print(memAddr + " limit switch state changed to " + state)
	pass # Replace with function body.


func _on_simulation_button_up() -> void:
	if(pullDataTimer.is_stopped()):
		pullDataTimer.start()
		simButton.text = "Stop Simulation"
	else:		
		pullDataTimer.stop()
		simButton.text = "Start Simulation"
	pass # Replace with function body.
