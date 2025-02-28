def before_OR(RLO, THIS, MEM):

	MEM[THIS["id"]] = 0
	return RLO

def before_OR_INPUT(RLO, THIS, MEM):
	return RLO
	
def OR(RLO, THIS, MEM):
	return RLO

def after_OR_INPUT(RLO, THIS, MEM):

	if "childId" in THIS:
		MEM[THIS["id"]] = MEM[THIS["id"]] | MEM[THIS["childId"]]
	return RLO

def after_OR(RLO, THIS, MEM):

	if "parentInputId" in THIS:
		RLO[THIS["parentInputId"]] = MEM[THIS["id"]] 

	RLO[THIS["id"]] = MEM[THIS["id"]]
	return RLO
	