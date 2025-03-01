def before_NOT(RLO, THIS, MEM):

	MEM[THIS["id"]] = 0
	return RLO

def before_NOT_INPUT(RLO, THIS, MEM):
	return RLO

def NOT(RLO, THIS, MEM):
	return RLO

def after_NOT_INPUT(RLO, THIS, MEM):
	if RLO[THIS["childId"]] == 1:
		MEM[THIS["id"]] = 0
	else:
		MEM[THIS["id"]] = 1
	return RLO

def after_NOT(RLO, THIS, MEM):
	RLO[THIS["id"]] = MEM[THIS["id"]]
	RLO[THIS["parentInputId"]] = MEM[THIS["id"]]
	return RLO