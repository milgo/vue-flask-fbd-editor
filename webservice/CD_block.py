def setup_CD (THIS, MEM):
	MEM[THIS["memoryAddr"]]["edge"] = 0

def before_CD(RLO, THIS, MEM):
    return RLO

def before_CD_INPUT(RLO, INPUT, MEM):
	return RLO

def CD(RLO, THIS, MEM):
	return RLO

def after_CD_INPUT(RLO, INPUT, MEM):
    if INPUT["inputName"] in ["DEC"]:
        if RLO[INPUT["connNodeId"]] == 1:
            if MEM[INPUT["memoryAddr"]]["edge"] == 0:
                MEM[INPUT["memoryAddr"]]["value"] = MEM[INPUT["memoryAddr"]]["value"] - 1
                MEM[INPUT["memoryAddr"]]["monitorData"] = MEM[INPUT["memoryAddr"]]["value"]
                MEM[INPUT["memoryAddr"]]["edge"] = 1
        else:
            MEM[INPUT["memoryAddr"]]["edge"] = 0

    if INPUT["inputName"] in ["R"]:
        if RLO[INPUT["connNodeId"]] == 1:
            MEM[INPUT["memoryAddr"]]["value"] = 0
            MEM[INPUT["memoryAddr"]]["monitorData"] = 0
    return RLO

def after_CD(RLO, THIS, MEM):
	return RLO