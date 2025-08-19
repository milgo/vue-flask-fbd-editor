def before_ADD(RLO, THIS, MEM):
    MEM[THIS["id"]] = 0 
    return RLO

def before_ADD_INPUT(RLO, INPUT, MEM):
    return RLO

def ADD(RLO, THIS, MEM):
    return RLO

def after_ADD_INPUT(RLO, INPUT, MEM):
    if "connNodeId" in INPUT:
        MEM[INPUT["id"]] = MEM[INPUT["id"]] + RLO[INPUT["connNodeId"]]
    return RLO

def after_ADD(RLO, THIS, MEM):
    RLO[THIS["id"]] = MEM[THIS["id"]]
    return RLO