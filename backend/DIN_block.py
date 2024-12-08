def before_DIN(RLO_obj, BLOCK_obj, MEM_obj):
	return RLO_obj

def DIN(RLO_obj, BLOCK_obj, MEM_obj):
	if MEM_obj[BLOCK_obj["memory"]]["type"] in ["di"]:
		pass
	if MEM_obj[BLOCK_obj["memory"]]["type"] in ["marker"]:
		pass
	MEM_obj[BLOCK_obj["input"]] = MEM_obj[BLOCK_obj["memory"]]["value"] 
	MEM_obj[BLOCK_obj["target"]] = MEM_obj[BLOCK_obj["memory"]]["value"]
	return RLO_obj

def after_DIN(RLO_obj, BLOCK_obj, MEM_obj):
	RLO_obj[BLOCK_obj["input"]] = MEM_obj[BLOCK_obj["input"]]
	RLO_obj[BLOCK_obj["target"]] = MEM_obj[BLOCK_obj["target"]]
	return RLO_obj
