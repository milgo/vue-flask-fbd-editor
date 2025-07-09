def before_OR(RLO, THIS, MEM):

	MEM[THIS["id"]] = 0
	return RLO

def before_OR_INPUT(RLO, INPUT, MEM):
	return RLO
	
def OR(RLO, THIS, MEM):
	return RLO

def after_OR_INPUT(RLO, INPUT, MEM):

	if "connNodeId" in INPUT:
		MEM[INPUT["id"]] = MEM[INPUT["id"]] | RLO[INPUT["connNodeId"]]
	return RLO

def after_OR(RLO, THIS, MEM):

	#RLO[THIS["destInputId"]] = MEM[THIS["id"]] 

	RLO[THIS["id"]] = MEM[THIS["id"]]
	return RLO
	