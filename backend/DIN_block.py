def before_DIN(RLO, THIS, MEM):
	#MEM[THIS["destInputId"]] = MEM[THIS["memoryAddr"]]["value"] 
	MEM[THIS["id"]] = MEM[THIS["memoryAddr"]]["value"]
	return RLO

def DIN(RLO, THIS, MEM):
	return RLO

def after_DIN(RLO, THIS, MEM):
	#RLO[THIS["destInputId"]] = MEM[THIS["id"]]
	RLO[THIS["id"]] = MEM[THIS["id"]]
	return RLO
