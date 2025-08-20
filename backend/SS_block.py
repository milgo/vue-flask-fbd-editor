import time

def current_milli_time():
    return round(time.time() * 1000)

def setup_SS(THIS, MEM):
    MEM[THIS["memoryAddr"]]["started"] = 0
    MEM[THIS["memoryAddr"]]["stopped"] = 0 

def before_SS(RLO, THIS, MEM):

    if "started" in MEM[THIS["memoryAddr"]] and MEM[THIS["memoryAddr"]]["started"] == 1:

        if "startTime" in MEM[THIS["memoryAddr"]] and MEM[THIS["memoryAddr"]]["stopped"] == 0:
            MEM[THIS["memoryAddr"]]["elapsedTime"] = (current_milli_time() - MEM[THIS["memoryAddr"]]["startTime"])
		
        if MEM[THIS["memoryAddr"]]["elapsedTime"] < MEM[THIS["memoryAddr"]]["duration"]:
            RLO[THIS["id"]] = 0
        else:
            RLO[THIS["id"]] = 1
            MEM[THIS["memoryAddr"]]["stopped"] = 1

    return RLO

def before_SS_INPUT(RLO, INPUT, MEM):
	return RLO

def SS(RLO, THIS, MEM):
	return RLO

def after_SS_INPUT(RLO, INPUT, MEM):

	if INPUT["inputName"] in ["S"]:

		if (RLO[INPUT["connNodeId"]] == 1) and (MEM[INPUT["memoryAddr"]]["started"] == 0):
			MEM[INPUT["memoryAddr"]]["started"] = 1
			MEM[INPUT["memoryAddr"]]["startTime"] = current_milli_time()

	if INPUT["inputName"] in ["R"] and RLO[INPUT["connNodeId"]] == 1 and MEM[INPUT["memoryAddr"]]["started"] == 1:
	
		MEM[INPUT["memoryAddr"]]["started"] = 0
		MEM[INPUT["memoryAddr"]]["elapsedTime"] = 0
		MEM[INPUT["memoryAddr"]]["stopped"] = 0
		RLO[INPUT["id"]] = 0
		
	if INPUT["inputName"] in ["T"]:
	
		MEM[INPUT["memoryAddr"]]["duration"] = RLO[INPUT["connNodeId"]]

	return RLO

def after_SS(RLO, THIS, MEM):
	return RLO