from src.states.level1 import Level1
from src.states.level2 import Level2

def setup_state(state_name):
    if state_name == "level1":
        return Level1()
    elif state_name == "level2":
        return Level2()
    else:
        raise ValueError(f"Unknown state: {state_name}")
