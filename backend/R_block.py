def before_R(RLO, THIS, MEM):

	MEM[THIS["id"]] = 0
	return RLO

def before_R_INPUT(RLO, THIS, MEM):
	return RLO

def R(RLO, THIS, MEM):
	return RLO

def after_R_INPUT(RLO, THIS, MEM):
	if MEM[THIS["childId"]] == 1:
		MEM[THIS["memoryAddr"]]["value"] = 0
	return RLO

def after_R(RLO, THIS, MEM):
	
	if MEM[THIS["memoryAddr"]]['forced'] == True:
		MEM[THIS["memoryAddr"]]["value"] = MEM[THIS["memoryAddr"]]["forcedValue"]

	RLO[THIS["id"]] = MEM[THIS["memoryAddr"]]["value"]

	return RLO