extends Node3D

var _goingUp : bool
var _goingDown : bool
var _speed = 2.0

func _ready() -> void:
	_goingUp = false
	_goingDown = false

func _on_logic_variable_value_changed(memAddr: String, oldval: String, newval: String) -> void:
	print("testing 123: "+memAddr+" "+newval)
	if memAddr.to_lower() == "%o1":
		if newval == "1.0":
			_goingUp = true
			_goingDown = false
		if newval == "0.0":
			_goingUp = false
			_goingDown = false
		
	if memAddr.to_lower() == "%o2":
		if newval == "1.0":
			_goingUp = false
			_goingDown = true
		if newval == "0.0":
			_goingUp = false
			_goingDown = false
			
	pass # Replace with function body.

func _process(delta: float) -> void:
	if _goingUp == true and position.y <= 15.0:
		position.y += _speed * delta
		if position.y > 15.0:
			position.y = 15.0
					
	if _goingDown == true and position.y >= 0.0:
		position.y -= _speed * delta
		if position.y < 0.0:
			position.y = 0.0
		
