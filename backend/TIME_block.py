def before_TIME(RLO, THIS, MEM):
	#MEM[THIS["destInputId"]] = MEM[THIS["memoryAddr"]]["value"] 
	MEM[THIS["id"]] = int(THIS["memoryAddr"])
	print(THIS)
	return RLO

def TIME(RLO, THIS, MEM):
	return RLO

def after_TIME(RLO, THIS, MEM):
	#RLO[THIS["destInputId"]] = MEM[THIS["id"]]
	RLO[THIS["id"]] = MEM[THIS["id"]]
	return RLO
