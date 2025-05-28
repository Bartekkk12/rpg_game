import pygame

class Weapon:
    def __init__(self, tier, attack_speed, weapon_range, image_path):
        self.tier = tier
        self.attack_speed = attack_speed
        self.range = weapon_range
        self.image = pygame.transform.scale(pygame.image.load(image_path), (50, 50))
        
class Melee_Weapon(Weapon):
    def __init__(self, tier, attack_speed, weapon_range, image_path, melee_damage):
        super().__init__(tier, attack_speed, weapon_range, image_path)
        self.melee_damage = melee_damage

class Ranged_Weapon(Weapon):
    def __init__(self, tier, attack_speed, weapon_range, image_path, ranged_damage, projectile_speed):
        super().__init__(tier, attack_speed, weapon_range, image_path)
        self.ranged_damage = ranged_damage
        self.projectile_speed = projectile_speed

class Magic_Weapon(Weapon):
    def __init__(self, tier, attack_speed, weapon_range, image_path, magic_damage, projectile_speed):
        super().__init__(tier, attack_speed, weapon_range, image_path)
        self.magic_damage = magic_damage
        self.projectile_speed = projectile_speed