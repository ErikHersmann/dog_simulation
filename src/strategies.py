from enum import Enum

class strategy_enum(Enum):
    RANDOM = 0
    MINMAX = 1
    GREEDY = 2
    
    
class move_type(Enum):
    NORMAL = 0
    MOVE_OUT_FROM_START = 1
    MOVE_INTO_SAFE_HOUSE = 2
    MULTI_MOVE = 3
    TELEPORT = 4
    
    
class move():
    """A move definition
    the source location is specified as the id of the tile or -1 if it's from the start of palyer 1 and -2 for player 2 etc
    the safe house locations are defined as 100 101 102 103 for player 1
    and 200 201 202 203 for player 2 etc
    """
    def __init__(self, source, target, captures, mtype):
        self.source_location = source
        self.target_location = target
        self.captures = captures
        self.move_type = mtype