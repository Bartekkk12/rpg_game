import pygame

ITEMS = {
    "hp_potion": {"base_price": 2, "max_hp_gain_value": 8, "image_path": "src/sprites/items/hp_potion.png"},
    "heart_of_renewal": {"base_price": 2, "hp_regen_gain_value": 1, "image_path": "src/sprites/items/heart_of_renewal.png"},
    "magic_amulet": {"base_price": 5, "magic_damage_gain_value": 5, "image_path": "src/sprites/items/magic_amulet.png"},
    "magic_spell": {"base_price": 1, "magic_damage_gain_value": 1, "image_path": "src/sprites/items/magic_spell.png"},
    "vest": {"base_price": 5, "max_armor_gain_value": 3, "image_path": "src/sprites/items/vest.png"},
    "glove_of_fury": {"base_price": 1, "attack_speed_gain_value": 1.2, "image_path": "src/sprites/items/glove_of_fury.png"},
}

class Item:
    def __init__(self, item_type):
        self.item_type = ITEMS[item_type]
        self.image = pygame.transform.scale(pygame.image.load(self.item_type["image_path"]), (150, 150))
        
    def apply_upgrades(self, player):
        for key, value in self.item_type.items():
            if key.endswith("_gain_value"):
                stat = key.replace("_gain_value", "")
                if hasattr(player, stat):
                    setattr(player, stat, getattr(player, stat) + value)