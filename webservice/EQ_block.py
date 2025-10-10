def setup_EQ(THIS, MEM):
    MEM[THIS["id"]] = {}
    MEM[THIS["id"]]["valueA"] = 0
    MEM[THIS["id"]]["valueB"] = 0

def before_EQ(RLO, THIS, MEM):
    return RLO

def before_EQ_INPUT(RLO, INPUT, MEM):
    return RLO

def EQ(RLO, THIS, MEM):
    return RLO

def after_EQ_INPUT(RLO, INPUT, MEM):
    print(MEM)
    if INPUT["inputName"] in ["IN1"]:
        MEM[INPUT["id"]]["valueA"] = RLO[INPUT["connNodeId"]]

    if INPUT["inputName"] in ["IN2"]:
        MEM[INPUT["id"]]["valueB"] = RLO[INPUT["connNodeId"]]
    return RLO

def after_EQ(RLO, THIS, MEM):
    RLO[THIS["id"]] = MEM[THIS["id"]]["valueA"] == MEM[THIS["id"]]["valueB"] 
    return RLO