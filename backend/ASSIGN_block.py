def pre_ASSIGN(RLO_obj, BLOCK_obj, MEM_obj):
	RLO_obj["STACK"].append(RLO_obj["RLO"])
	return RLO_obj
	
def ASSIGN(RLO_obj, BLOCK_obj, MEM_obj):
	print("{" )
	#ASSIGN VALUE TO MEM_obj
	print("}")
	return RLO_obj
	
def post_ASSIGN(RLO_obj, BLOCK_obj, MEM_obj):
	RLO_obj["RLO"] = RLO_obj["STACK"].pop()
	RLO_obj[BLOCK_obj["target"]] = RLO_obj["RLO"]
	print("\ttarget = " + str(RLO_obj[BLOCK_obj["target"]]))
	return RLO_obj