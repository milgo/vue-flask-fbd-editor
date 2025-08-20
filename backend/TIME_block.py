def before_TIME(RLO, THIS, MEM):
	MEM[THIS["id"]] = int(THIS["memoryAddr"])
	return RLO

def TIME(RLO, THIS, MEM):
	return RLO

def after_TIME(RLO, THIS, MEM):
	RLO[THIS["id"]] = MEM[THIS["id"]]
	return RLO
