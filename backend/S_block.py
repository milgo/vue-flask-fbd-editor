def before_S(RLO, THIS, MEM):

	MEM[THIS["id"]] = 0
	return RLO

def before_S_INPUT(RLO, THIS, MEM):
	return RLO

def S(RLO, THIS, MEM):
	return RLO

def after_S_INPUT(RLO, THIS, MEM):
	if RLO[THIS["childId"]] == 1:
		MEM[THIS["memoryAddr"]]["value"] = 1
	return RLO

def after_S(RLO, THIS, MEM):
	
	if MEM[THIS["memoryAddr"]]["forced"] == True:
		MEM[THIS["memoryAddr"]]["value"] = MEM[THIS["memoryAddr"]]["forcedValue"]

	RLO[THIS["id"]] = MEM[THIS["memoryAddr"]]["value"]
	RLO[THIS["parentInputId"]] = MEM[THIS["memoryAddr"]]["value"]
	
	return RLO