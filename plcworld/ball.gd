extends Node3D

@onready var timer: Timer = $Timer

func _ready() -> void:
	timer.timeout.connect(_on_timeout)
	timer.start()
	pass # Replace with function body.

func _on_timeout() -> void:
	#print("tick")
	queue_free()
	pass
