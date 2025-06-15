import random

from item import ITEMS
from weapon import WEAPONS

class Shop:
    def __init__(self):
        self.MAX_ITEMS = 4
        self.available_item_keys = list(ITEMS.keys())
        self.current_items = []
        
    def roll_items(self, player):
        available_weapons = [w for w in WEAPONS.keys() if w not in player.weapons or player.weapons[w].level < 4]
        if not available_weapons:
            weapon_key = random.choice(list(WEAPONS.keys()))
        else:
            weapon_key = random.choice(available_weapons)

        # random items
        item_keys = list(ITEMS.keys())
        random.shuffle(item_keys)
        item_keys = item_keys[:3]

        self.current_items = [weapon_key] + item_keys