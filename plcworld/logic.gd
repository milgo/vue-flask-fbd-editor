extends Node

var _setupListing
var _programListing

func execute(json):
	print(str("Logic command: ", json["command"]))
	
	_setupListing = json["data"]["setuplisting"]
	_programListing = json["data"]["listing"]
	
	print(str(_setupListing))
	print(str(_programListing))
	
	for setup in _setupListing:
		call(setup["functionName"], setup)
	
	pass

func _process(_delta: float) -> void:
	pass


func setup_DIN(_jsonData):
	print(_jsonData)
	pass
