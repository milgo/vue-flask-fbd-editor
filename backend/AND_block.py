def before_AND(RLO_obj, BLOCK_obj, MEM_obj):

	MEM_obj[BLOCK_obj["target"]] = 1
	return RLO_obj

def before_AND_INPUT(RLO_obj, BLOCK_obj, MEM_obj):
	return RLO_obj
	
def AND(RLO_obj, BLOCK_obj, MEM_obj):
	return RLO_obj

def after_AND_INPUT(RLO_obj, BLOCK_obj, MEM_obj):

	if "inputNode" in BLOCK_obj:
		MEM_obj[BLOCK_obj["target"]] = MEM_obj[BLOCK_obj["target"]] & MEM_obj[BLOCK_obj["inputNode"]]
	return RLO_obj

def after_AND(RLO_obj, BLOCK_obj, MEM_obj):

	if "input" in BLOCK_obj:
		RLO_obj[BLOCK_obj["input"]] = MEM_obj[BLOCK_obj["target"]] 

	RLO_obj[BLOCK_obj["target"]] = MEM_obj[BLOCK_obj["target"]]
	return RLO_obj
	