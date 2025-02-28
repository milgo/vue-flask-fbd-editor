def before_AND(RLO, THIS, MEM):

	MEM[THIS["id"]] = 1
	return RLO

def before_AND_INPUT(RLO, THIS, MEM):
	return RLO
	
def AND(RLO, THIS, MEM):
	return RLO

def after_AND_INPUT(RLO, THIS, MEM):

	if "childId" in THIS:
		MEM[THIS["id"]] = MEM[THIS["id"]] & MEM[THIS["childId"]]
	return RLO

def after_AND(RLO, THIS, MEM):

	if "parentInputId" in THIS:
		RLO[THIS["parentInputId"]] = MEM[THIS["id"]] 

	RLO[THIS["id"]] = MEM[THIS["id"]]
	return RLO
	