def before_SR(RLO, THIS, MEM):

	MEM[THIS["id"]] = 0
	return RLO

def before_SR_INPUT(RLO, THIS, MEM):
	return RLO

def SR(RLO, THIS, MEM):
	return RLO

def after_SR_INPUT(RLO, THIS, MEM):

	if THIS["inputName"] in ["S"]:
		if RLO[THIS["childId"]] == 1:
			MEM[THIS["memoryAddr"]]["value"] = 1

	if THIS["inputName"] in ["R"]:
		if RLO[THIS["childId"]] == 1:			
			MEM[THIS["memoryAddr"]]["value"] = 0

	return RLO

def after_SR(RLO, THIS, MEM):
	
	if MEM[THIS["memoryAddr"]]["forced"] == True:
		MEM[THIS["memoryAddr"]]["value"] = MEM[THIS["memoryAddr"]]["forcedValue"]

	RLO[THIS["id"]] = MEM[THIS["memoryAddr"]]["value"]
	RLO[THIS["parentInputId"]] = MEM[THIS["memoryAddr"]]["value"]
	return RLO