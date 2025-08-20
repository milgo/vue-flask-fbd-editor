def before_RS(RLO, THIS, MEM):
	MEM[THIS["id"]] = 0
	return RLO

def before_RS_INPUT(RLO, INPUT, MEM):
	return RLO

def RS(RLO, THIS, MEM):
	return RLO

def after_RS_INPUT(RLO, INPUT, MEM):

	if INPUT["inputName"] in ["S"]:
		if RLO[INPUT["connNodeId"]] == 1:
			MEM[INPUT["memoryAddr"]]["value"] = 1

	if INPUT["inputName"] in ["R"]:
		if RLO[INPUT["connNodeId"]] == 1:			
			MEM[INPUT["memoryAddr"]]["value"] = 0

	return RLO

def after_RS(RLO, THIS, MEM):
	
	if MEM[THIS["memoryAddr"]]["forced"] == True:
		MEM[THIS["memoryAddr"]]["value"] = MEM[THIS["memoryAddr"]]["forcedValue"]

	RLO[THIS["id"]] = MEM[THIS["memoryAddr"]]["value"]
	#RLO[THIS["destInputId"]] = MEM[THIS["memoryAddr"]]["value"]

	return RLO