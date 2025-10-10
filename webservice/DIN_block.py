def before_DIN(RLO, THIS, MEM):
	MEM[THIS["id"]] = MEM[THIS["memoryAddr"]]["value"]
	return RLO

def DIN(RLO, THIS, MEM):
	return RLO

def after_DIN(RLO, THIS, MEM):
	#RLO[THIS["destInputId"]] = MEM[THIS["id"]]
	RLO[THIS["id"]] = MEM[THIS["id"]]
	if MEM[THIS["id"]] == 1:
		MEM[THIS["memoryAddr"]]["monitorData"] = "True"
	else:
		MEM[THIS["memoryAddr"]]["monitorData"] = "False"
	return RLO
