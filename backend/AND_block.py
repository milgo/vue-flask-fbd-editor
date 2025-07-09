def before_AND(RLO, THIS, MEM):

	MEM[THIS["id"]] = 1
	return RLO

def before_AND_INPUT(RLO, INPUT, MEM):
	return RLO
	
def AND(RLO, THIS, MEM):
	return RLO

def after_AND_INPUT(RLO, INPUT, MEM):

	if "connNodeId" in INPUT:
		MEM[INPUT["id"]] = MEM[INPUT["id"]] & RLO[INPUT["connNodeId"]]
	return RLO

def after_AND(RLO, THIS, MEM):

	#RLO[THIS["destInputId"]] = MEM[THIS["id"]] 

	RLO[THIS["id"]] = MEM[THIS["id"]]
	return RLO
	