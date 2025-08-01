import time

def current_milli_time():
    return round(time.time() * 1000)

def before_SF(RLO, THIS, MEM):

    MEM[THIS["id"]] = 0

    if not ("started" in MEM[THIS["memoryAddr"]]):
        MEM[THIS["memoryAddr"]]["started"] = 0        

    if "started" in MEM[THIS["memoryAddr"]] and MEM[THIS["memoryAddr"]]["started"] == 1:

        if "startTime" in MEM[THIS["memoryAddr"]]:
            MEM[THIS["memoryAddr"]]["elapsedTime"] = (current_milli_time() - MEM[THIS["memoryAddr"]]["startTime"])
		
        if MEM[THIS["memoryAddr"]]["elapsedTime"] < MEM[THIS["memoryAddr"]]["duration"]:
            MEM[THIS["id"]] = 0
        else:
            MEM[THIS["id"]] = 1

    return RLO

def before_SF_INPUT(RLO, INPUT, MEM):

	return RLO

def SF(RLO, THIS, MEM):
	return RLO

def after_SF_INPUT(RLO, INPUT, MEM):

	if INPUT["inputName"] in ["S"]:

		if (RLO[INPUT["connNodeId"]] == 0) and (MEM[INPUT["memoryAddr"]]["started"] == 0):
			MEM[INPUT["memoryAddr"]]["started"] = 1
			MEM[INPUT["memoryAddr"]]["startTime"] = current_milli_time()

		if RLO[INPUT["connNodeId"]] == 1:
			MEM[INPUT["memoryAddr"]]["started"] = 0
			MEM[INPUT["id"]] = 0

	if INPUT["inputName"] in ["R"] and RLO[INPUT["connNodeId"]] == 1 and MEM[INPUT["memoryAddr"]]["started"] == 1:
	
		MEM[INPUT["memoryAddr"]]["started"] = 0
		MEM[INPUT["memoryAddr"]]["elapsedTime"] = 0
		RLO[INPUT["id"]] = 0
		
	if INPUT["inputName"] in ["T"]:
	
		MEM[INPUT["memoryAddr"]]["duration"] = RLO[INPUT["connNodeId"]]

	return RLO

def after_SF(RLO, THIS, MEM):

    if THIS["id"] in RLO:
        if MEM[THIS["id"]] == 1:
	        RLO[THIS["id"]] = 0
        else:
            RLO[THIS["id"]] = 1
    return RLO