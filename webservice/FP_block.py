def before_FP(RLO, THIS, MEM):
	MEM[THIS["id"]] = 0
	return RLO

def before_FP_INPUT(RLO, INPUT, MEM):
	return RLO

def FP(RLO, THIS, MEM):
	return RLO

def after_FP_INPUT(RLO, INPUT, MEM):

	if RLO[INPUT["connNodeId"]] == 1 and MEM[INPUT["memoryAddr"]]["value"] == 0:
		MEM[INPUT["id"]] = 1
		
	MEM[INPUT["memoryAddr"]]["value"] = RLO[INPUT["connNodeId"]]
	return RLO

def after_FP(RLO, THIS, MEM):
	RLO[THIS["id"]] = MEM[THIS["id"]]
	#RLO[THIS["destInputId"]] = MEM[THIS["id"]]
	return RLO