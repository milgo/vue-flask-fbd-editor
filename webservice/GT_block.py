def setup_GT(THIS, MEM):
    MEM[THIS["id"]] = {}
    MEM[THIS["id"]]["valueA"] = 0
    MEM[THIS["id"]]["valueB"] = 0

def before_GT(RLO, THIS, MEM):
    return RLO

def before_GT_INPUT(RLO, INPUT, MEM):
    return RLO

def GT(RLO, THIS, MEM):
    return RLO

def after_GT_INPUT(RLO, INPUT, MEM):
    if INPUT["inputName"] in ["IN1"]:
        MEM[INPUT["id"]]["valueA"] = RLO[INPUT["connNodeId"]]

    if INPUT["inputName"] in ["IN2"]:
        MEM[INPUT["id"]]["valueB"] = RLO[INPUT["connNodeId"]]
    return RLO

def after_GT(RLO, THIS, MEM):
    RLO[THIS["id"]] = MEM[THIS["id"]]["valueA"] > MEM[THIS["id"]]["valueB"] 
    return RLO