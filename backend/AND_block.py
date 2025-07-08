def before_AND(RLO, THIS, MEM):

	MEM[THIS["id"]] = 1
	return RLO

def before_AND_INPUT(RLO, INPUT, MEM):
	return RLO
	
def AND(RLO, THIS, MEM):
	return RLO

def after_AND_INPUT(RLO, INPUT, MEM):

	if "sourceNodeId" in INPUT:
		MEM[INPUT["id"]] = MEM[INPUT["id"]] & RLO[INPUT["sourceNodeId"]]
	return RLO

def after_AND(RLO, THIS, MEM):

	RLO[THIS["destInputId"]] = MEM[THIS["id"]] 

	RLO[THIS["id"]] = MEM[THIS["id"]]
	return RLO
	