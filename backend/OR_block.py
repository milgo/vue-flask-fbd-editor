def before_OR(RLO_obj, BLOCK_obj, MEM_obj):

	MEM_obj[BLOCK_obj["target"]] = 0
	return RLO_obj

def before_OR_INPUT(RLO_obj, BLOCK_obj, MEM_obj):
	return RLO_obj
	
def OR(RLO_obj, BLOCK_obj, MEM_obj):
	return RLO_obj

def after_OR_INPUT(RLO_obj, BLOCK_obj, MEM_obj):

	if "inputNode" in BLOCK_obj:
		MEM_obj[BLOCK_obj["target"]] = MEM_obj[BLOCK_obj["target"]] | MEM_obj[BLOCK_obj["inputNode"]]
	return RLO_obj

def after_OR(RLO_obj, BLOCK_obj, MEM_obj):

	if "input" in BLOCK_obj:
		RLO_obj[BLOCK_obj["input"]] = MEM_obj[BLOCK_obj["target"]] 

	RLO_obj[BLOCK_obj["target"]] = MEM_obj[BLOCK_obj["target"]]
	return RLO_obj
	