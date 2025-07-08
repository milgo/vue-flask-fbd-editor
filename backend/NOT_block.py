def before_NOT(RLO, THIS, MEM):

	MEM[THIS["id"]] = 0
	return RLO

def before_NOT_INPUT(RLO, INPUT, MEM):
	return RLO

def NOT(RLO, THIS, MEM):
	return RLO

def after_NOT_INPUT(RLO, INPUT, MEM):
	if RLO[INPUT["sourceNodeId"]] == 1:
		MEM[INPUT["id"]] = 0
	else:
		MEM[INPUT["id"]] = 1
	return RLO

def after_NOT(RLO, THIS, MEM):
	RLO[THIS["id"]] = MEM[THIS["id"]]
	RLO[THIS["destInputId"]] = MEM[THIS["id"]]
	return RLO