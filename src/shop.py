import random

from item import ITEMS
from weapon import WEAPONS

class Shop:
    def __init__(self):
        self.MAX_ITEMS = 4
        self.available_item_keys = list(ITEMS.keys())
        self.current_items = []

    def roll_items(self, player):
        self.current_items = []

        if len(player.weapons) < 4:
            # Losuj nową broń
            missing_weapons = [w for w in WEAPONS.keys() if w not in player.weapons]
            if missing_weapons:
                weapon_key = random.choice(missing_weapons)
                self.current_items.append(weapon_key)
                # 3 itemy
                item_keys = list(ITEMS.keys())
                random.shuffle(item_keys)
                self.current_items += item_keys[:3]
            else:
                # Wszystkie bronie, ale to fallback - powinno być rzadkie
                item_keys = list(ITEMS.keys())
                random.shuffle(item_keys)
                self.current_items += item_keys[:4]
        else:
            upgradable_weapons = [key for key, w in player.weapons.items() if w.level < 4]
            if upgradable_weapons:
                weapon_key = random.choice(upgradable_weapons)
                self.current_items.append(weapon_key)
                item_keys = list(ITEMS.keys())
                random.shuffle(item_keys)
                self.current_items += item_keys[:3]
            else:
                # WSZYSTKO WYMAXOWANE: sklep = 4 itemy!
                item_keys = list(ITEMS.keys())
                random.shuffle(item_keys)
                self.current_items = item_keys[:4]