def before_MUL(RLO, THIS, MEM):
    MEM[THIS["id"]] = 1 
    return RLO

def before_MUL_INPUT(RLO, INPUT, MEM):
    return RLO

def MUL(RLO, THIS, MEM):
    return RLO

def after_MUL_INPUT(RLO, INPUT, MEM):
    if "connNodeId" in INPUT:
        MEM[INPUT["id"]] = MEM[INPUT["id"]] * RLO[INPUT["connNodeId"]]
    return RLO

def after_MUL(RLO, THIS, MEM):
    RLO[THIS["id"]] = MEM[THIS["id"]]
    return RLO