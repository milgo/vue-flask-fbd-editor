def before_MOVE(RLO, THIS, MEM):

	MEM[THIS["id"]] = 0
	return RLO

def before_MOVE_INPUT(RLO, INPUT, MEM):
	return RLO

def MOVE(RLO, THIS, MEM):
	return RLO

def after_MOVE_INPUT(RLO, INPUT, MEM):

	MEM[INPUT["memoryAddr"]]["value"] = RLO[INPUT["connNodeId"]]
	return RLO

def after_MOVE(RLO, THIS, MEM):
	
	RLO[THIS["id"]] = MEM[THIS["memoryAddr"]]["value"]
	
	return RLO