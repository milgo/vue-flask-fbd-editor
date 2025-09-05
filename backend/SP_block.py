import time

def current_milli_time():
    return round(time.time() * 1000)

def setup_SP(THIS, MEM):
    MEM[THIS["memoryAddr"]]["started"] = 0
    MEM[THIS["memoryAddr"]]["stopped"] = 0 
    
def before_SP(RLO, THIS, MEM):
            
    if "started" in MEM[THIS["memoryAddr"]] and MEM[THIS["memoryAddr"]]["started"] == 1:
        if "startTime" in MEM[THIS["memoryAddr"]] and MEM[THIS["memoryAddr"]]["stopped"] == 0:
            MEM[THIS["memoryAddr"]]["elapsedTime"] = (current_milli_time() - MEM[THIS["memoryAddr"]]["startTime"])
            MEM[THIS["memoryAddr"]]["monitorData"] = MEM[THIS["memoryAddr"]]["duration"] - MEM[THIS["memoryAddr"]]["elapsedTime"]

        if MEM[THIS["memoryAddr"]]["elapsedTime"] < MEM[THIS["memoryAddr"]]["duration"]:
            MEM[THIS["memoryAddr"]]["value"] = 1
        else:
            MEM[THIS["memoryAddr"]]["value"] = 0
            MEM[THIS["memoryAddr"]]["stopped"] = 1 
            MEM[THIS["memoryAddr"]]["monitorData"] = 0
    return RLO

def before_SP_INPUT(RLO, INPUT, MEM):

	return RLO

def SP(RLO, THIS, MEM):
	return RLO

def after_SP_INPUT(RLO, INPUT, MEM):

	if INPUT["inputName"] in ["S"]:

		if (RLO[INPUT["connNodeId"]] == 1) and (MEM[INPUT["memoryAddr"]]["started"] == 0):
			MEM[INPUT["memoryAddr"]]["started"] = 1
			MEM[INPUT["memoryAddr"]]["startTime"] = current_milli_time()

		if RLO[INPUT["connNodeId"]] == 0:
			MEM[INPUT["memoryAddr"]]["started"] = 0
			MEM[INPUT["memoryAddr"]]["stopped"] = 0 
			RLO[INPUT["id"]] = 0

	if INPUT["inputName"] in ["R"] and RLO[INPUT["connNodeId"]] == 1 and MEM[INPUT["memoryAddr"]]["started"] == 1:
	
		MEM[INPUT["memoryAddr"]]["started"] = 0
		MEM[INPUT["memoryAddr"]]["elapsedTime"] = 0
		RLO[INPUT["id"]] = 0
		
	if INPUT["inputName"] in ["T"]:
		MEM[INPUT["memoryAddr"]]["duration"] = RLO[INPUT["connNodeId"]]

	#print(RLO)

	return RLO

def after_SP(RLO, THIS, MEM):
	RLO[THIS["id"]] = MEM[THIS["memoryAddr"]]["value"]
	#RLO[THIS["destInputId"]] = MEM[THIS["id"]]
	return RLO