import pygame

ITEMS = {
    "hp_potion": {"base_price": 20, "hp_gain_value": 8, "image_path": "src/sprites/items/hp_potion.png"},
    "heart_of_renewal": {"base_price": 25, "hp_regen_gain_value": 1, "image_path": "src/sprites/items/heart_of_renewal.png"},
    "magic_amulet": {"base_price": 50, "magic_damage_gain_value": 5, "image_path": "src/sprites/items/magic_amulet.png"},
    "magic_spell": {"base_price": 15, "magic_damage_gain_value": 1, "image_path": "src/sprites/items/magic_spell.png"},
    "vest": {"base_price": 50, "armor_gain_value": 3, "image_path": "src/sprites/items/vest.png"},
    "glove_of_fury": {"base_price": 120, "attack_speed_gain_value": 1.2, "image_path": "src/sprites/items/glove_of_fury.png"},
}

class Item:
    def __init__(self, item_type, image_path=None):
        self.item_type = ITEMS[item_type]
        self.image = pygame.transform.scale(pygame.image.load(self.item_type[image_path]), (150, 150))