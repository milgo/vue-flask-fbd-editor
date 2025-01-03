def before_ASSIGN(RLO_obj, BLOCK_obj, MEM_obj):

	MEM_obj[BLOCK_obj["target"]] = 0
	return RLO_obj

def before_ASSIGN_INPUT(RLO_obj, BLOCK_obj, MEM_obj):
	return RLO_obj

def ASSIGN(RLO_obj, BLOCK_obj, MEM_obj):

	return RLO_obj

def after_ASSIGN_INPUT(RLO_obj, BLOCK_obj, MEM_obj):
	MEM_obj[BLOCK_obj["target"]] = MEM_obj[BLOCK_obj["inputNode"]]
	return RLO_obj

def after_ASSIGN(RLO_obj, BLOCK_obj, MEM_obj):
	
	if MEM_obj[BLOCK_obj["memory"]]['forced'] == True:
		MEM_obj[BLOCK_obj["memory"]]["value"] = MEM_obj[BLOCK_obj["memory"]]["forcedValue"]
	else:
		MEM_obj[BLOCK_obj["memory"]]["value"] = MEM_obj[BLOCK_obj["target"]]

	RLO_obj[BLOCK_obj["target"]] = MEM_obj[BLOCK_obj["memory"]]["value"]

	return RLO_obj