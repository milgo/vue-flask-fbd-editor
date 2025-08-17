def before_CONST(RLO, THIS, MEM):
    MEM[THIS["memoryAddr"]]["value"] = int(THIS["memoryAddr"]) 
    return RLO

def before_CONST_INPUT(RLO, INPUT, MEM):
    return RLO

def CONST(RLO, THIS, MEM):
    return RLO

def after_CONST_INPUT(RLO, INPUT, MEM):
    return RLO

def after_CONST(RLO, THIS, MEM):
    RLO[THIS["id"]] = MEM[THIS["memoryAddr"]]["value"]
    return RLO