import re
def setup_TIME(THIS, MEM):
	MEM[THIS["id"]] = int(re.findall("\\d{1,6}", THIS["memoryAddr"])[0])
	print(MEM[THIS["id"]])

def before_TIME(RLO, THIS, MEM):
	return RLO

def TIME(RLO, THIS, MEM):
	return RLO

def after_TIME(RLO, THIS, MEM):
	RLO[THIS["id"]] = MEM[THIS["id"]]
	return RLO
