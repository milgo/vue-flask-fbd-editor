extends Area3D

signal show_description(desc)
signal state_changed(memAddr, state)
@export var description:String
@export var memAddr:String

func _process(delta: float) -> void:
	pass

func _on_mouse_entered() -> void:
	show_description.emit(memAddr+" - "+description)
	pass

func _on_body_entered(body: Node3D) -> void:
	state_changed.emit(memAddr, "1")
	pass


func _on_body_exited(body: Node3D) -> void:
	state_changed.emit(memAddr, "0")
	pass
