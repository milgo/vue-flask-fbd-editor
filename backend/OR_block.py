def pre_OR(RLO_obj, BLOCK_obj, MEM_obj):
	RLO_obj["STACK"].append(RLO_obj["RLO"])
	RLO_obj["RLO"] = 0
	return RLO_obj
	
def OR(RLO_obj, BLOCK_obj, MEM_obj):
	print("{" )
	RLO = RLO_obj["RLO"]
	print("\tRLO (before) = " + str(RLO))
	RLO = RLO | MEM_obj[BLOCK_obj["memory"]]
	print("\tRLO (after) = " + str(RLO))
	RLO_obj[BLOCK_obj["target"]] = RLO
	#print("\ttarget = " + str(RLO_obj[BLOCK_obj["target"]]))
	RLO_obj["RLO"] = RLO
	print("}")
	return RLO_obj
	
def post_OR(RLO_obj, BLOCK_obj, MEM_obj):
	print("\ttarget = " + str(RLO_obj[BLOCK_obj["target"]]))
	RLO_obj["RLO"] = RLO_obj[BLOCK_obj["target"]] | RLO_obj["STACK"].pop()
	return RLO_obj