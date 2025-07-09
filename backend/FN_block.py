def before_FN(RLO, THIS, MEM):

	MEM[THIS["id"]] = 0
	return RLO

def before_FN_INPUT(RLO, INPUT, MEM):
	return RLO

def FN(RLO, THIS, MEM):
	return RLO

def after_FN_INPUT(RLO, INPUT, MEM):

	if RLO[INPUT["connNodeId"]] == 0 and MEM[INPUT["memoryAddr"]]["value"] == 1:
		MEM[INPUT["id"]] = 1
		
	MEM[INPUT["memoryAddr"]]["value"] = RLO[INPUT["connNodeId"]]
	return RLO

def after_FN(RLO, THIS, MEM):
	RLO[THIS["id"]] = MEM[THIS["id"]]
	#RLO[THIS["destInputId"]] = MEM[THIS["id"]]
	return RLO