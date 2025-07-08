def before_ASSIGN(RLO, THIS, MEM):

	MEM[THIS["id"]] = 0
	return RLO

def before_ASSIGN_INPUT(RLO, INPUT, MEM):
	return RLO

def ASSIGN(RLO, THIS, MEM):
	return RLO

def after_ASSIGN_INPUT(RLO, INPUT, MEM):
	MEM[INPUT["id"]] = RLO[INPUT["sourceNodeId"]]
	return RLO

def after_ASSIGN(RLO, THIS, MEM):
	
	if MEM[THIS["memoryAddr"]]["forced"] == True:
		MEM[THIS["memoryAddr"]]["value"] = MEM[THIS["memoryAddr"]]["forcedValue"]
	else:
		MEM[THIS["memoryAddr"]]["value"] = MEM[THIS["id"]]

	RLO[THIS["id"]] = MEM[THIS["memoryAddr"]]["value"]
	RLO[THIS["destInputId"]] = MEM[THIS["id"]] 
	return RLO