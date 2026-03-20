extends Node3D

@onready var _doormesh = $DoorMesh

var _opening : bool
var _closing : bool
var _speed = 2.0

func _ready() -> void:
	_opening = false
	_closing = false

func _on_logic_variable_value_changed(memAddr: String, oldval: Variant, newval: Variant) -> void:
	var newvalf = float(newval)
	if memAddr.to_lower() == get_meta("OPEN"):
		if newvalf == 1.0:
			_opening = true
			_closing = false
		if newvalf == 0.0:
			_opening = false
			_closing = false
	if memAddr.to_lower() == get_meta("CLOSE"):
		if newvalf == 1.0:
			_opening = false
			_closing = true
		if newvalf == 0.0:
			_opening = false
			_closing = false

func _process(delta: float) -> void:
	if _opening == true and _doormesh.position.z <= 1.0:
		_doormesh.position.z += _speed * delta
		if _doormesh.position.z > 1.0:
			_doormesh.position.z = 1.0
					
	if _closing == true and _doormesh.position.z >= 0.0:
		_doormesh.position.z -= _speed * delta
		if _doormesh.position.z < 0.0:
			_doormesh.position.z = 0.0
