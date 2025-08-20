def setup_CU(THIS, MEM):
    MEM[THIS["memoryAddr"]]["edge"] = 0

def before_CU(RLO, THIS, MEM):   	
    return RLO

def before_CU_INPUT(RLO, INPUT, MEM):
    return RLO

def CU(RLO, THIS, MEM):
    return RLO

def after_CU_INPUT(RLO, INPUT, MEM):
    if INPUT["inputName"] in ["INC"]:
        if RLO[INPUT["connNodeId"]] == 1:
            if MEM[INPUT["memoryAddr"]]["edge"] == 0:
                MEM[INPUT["memoryAddr"]]["value"] = MEM[INPUT["memoryAddr"]]["value"] + 1
                MEM[INPUT["memoryAddr"]]["monitorData"] = MEM[INPUT["memoryAddr"]]["value"]
                MEM[INPUT["memoryAddr"]]["edge"] = 1
        else:
            MEM[INPUT["memoryAddr"]]["edge"] = 0

    if INPUT["inputName"] in ["R"]:
        if RLO[INPUT["connNodeId"]] == 1:
            MEM[INPUT["memoryAddr"]]["value"] = 0
            MEM[INPUT["memoryAddr"]]["monitorData"] = 0
    return RLO

def after_CU(RLO, THIS, MEM):
    return RLO