from enum import Enum


class spot_base():
    def __init__(self, player_index, card_index):
        self.name = f"{player_index}_{card_index}"
        self.value = player_index*4 + card_index+1
        self.associated_player = player_index
        
    def __str__(self):
        return str(self.value)
        
class empty_spot(spot_base):
    def __init__(self):
        self.name = "0"
        self.value = 0
        self.associated_player = -1
    
    def __str__(self):
        return super().__str__()
        
class card_enum(Enum):
    TWO = 2
    THREE = 3
    FOUR_SPECIAL = 4
    FIVE = 5
    SIX = 6
    SEVEN_SPECIAL = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    ELEVEN_SPECIAL = 11
    TWELVE = 12
    THIRTEEN_SPECIAL = 13
    JOKER = 14
    TELEPORT = 15
        
        
class card_base():
    def __init__(self, id: int, value: card_enum):
        self.id = id
        self.value = value
        self.in_pool = True
        
    def __str__(self):
        return str(self.value)    