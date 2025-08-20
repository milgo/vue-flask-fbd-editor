def setup_LE(THIS, MEM):
    MEM[THIS["id"]] = {}
    MEM[THIS["id"]]["valueA"] = 0
    MEM[THIS["id"]]["valueB"] = 0

def before_LE(RLO, THIS, MEM):
    return RLO

def before_LE_INPUT(RLO, INPUT, MEM):
    return RLO

def LE(RLO, THIS, MEM):
    return RLO

def after_LE_INPUT(RLO, INPUT, MEM):
    if INPUT["inputName"] in ["IN1"]:
        MEM[INPUT["id"]]["valueA"] = RLO[INPUT["connNodeId"]]

    if INPUT["inputName"] in ["IN2"]:
        MEM[INPUT["id"]]["valueB"] = RLO[INPUT["connNodeId"]]
    return RLO

def after_LE(RLO, THIS, MEM):
    RLO[THIS["id"]] = MEM[THIS["id"]]["valueA"] <= MEM[THIS["id"]]["valueB"] 
    return RLO