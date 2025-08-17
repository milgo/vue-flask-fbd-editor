def before_GE(RLO, THIS, MEM):
    MEM[THIS["id"]] = {}
    if not ("valueA" in MEM[THIS["id"]]):
        MEM[THIS["id"]]["valueA"] = 0 
    if not ("valueB" in MEM[THIS["id"]]):
        MEM[THIS["id"]]["valueB"] = 0 
    return RLO

def before_GE_INPUT(RLO, INPUT, MEM):
    return RLO

def GE(RLO, THIS, MEM):
    return RLO

def after_GE_INPUT(RLO, INPUT, MEM):
    if INPUT["inputName"] in ["IN1"]:
        MEM[INPUT["id"]]["valueA"] = RLO[INPUT["connNodeId"]]

    if INPUT["inputName"] in ["IN2"]:
        MEM[INPUT["id"]]["valueB"] = RLO[INPUT["connNodeId"]]
    return RLO

def after_GE(RLO, THIS, MEM):
    RLO[THIS["id"]] = MEM[THIS["id"]]["valueA"] >= MEM[THIS["id"]]["valueB"] 
    return RLO