def before_DIV(RLO, THIS, MEM):
    MEM[THIS["id"]] = 0 
    return RLO

def before_DIV_INPUT(RLO, INPUT, MEM):
    return RLO

def DIV(RLO, THIS, MEM):
    return RLO

def after_DIV_INPUT(RLO, INPUT, MEM):
    if "connNodeId" in INPUT:
        if MEM[INPUT["id"]] == 0:
            MEM[INPUT["id"]] = RLO[INPUT["connNodeId"]]
        else:
            MEM[INPUT["id"]] = MEM[INPUT["id"]] / RLO[INPUT["connNodeId"]]
    return RLO

def after_DIV(RLO, THIS, MEM):
    RLO[THIS["id"]] = MEM[THIS["id"]]
    return RLO