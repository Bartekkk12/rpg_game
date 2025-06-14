import random

from item import ITEMS

class Shop:
    def __init__(self):
        self.MAX_ITEMS = 4
        self.available_item_keys = list(ITEMS.keys())
        self.current_items = []
        
    def roll_items(self):
        self.current_items = random.sample(self.available_item_keys, self.MAX_ITEMS)