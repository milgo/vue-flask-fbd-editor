def before_MARK(RLO_obj, BLOCK_obj, MEM_obj):
	return RLO_obj
	
def MARK(RLO_obj, BLOCK_obj, MEM_obj):
	RLO_obj[BLOCK_obj["input"]] = MEM_obj[BLOCK_obj["memory"]]["value"] 
	RLO_obj[BLOCK_obj["target"]] = MEM_obj[BLOCK_obj["memory"]]["value"]
	return RLO_obj

def after_MARK(RLO_obj, BLOCK_obj, MEM_obj):
	return RLO_obj
	