import pygame

class Weapon:
    def __init__(self, tier, attack_speed, range):
        self.tier = tier
        self.attack_speed = attack_speed
        self.range = range
        
class Melee_Weapon(Weapon):
    def __init__(self, tier, attack_speed, range, melee_damage):
        super().__init__(tier, attack_speed, range)
        self.melee_damage = melee_damage

class Ranged_Weapon(Weapon):
    def __init__(self, tier, attack_speed, range, ranged_damage, projectile_speed):
        super().__init__(tier, attack_speed, range)
        self.ranged_damage = ranged_damage
        self.projectile_speed = projectile_speed

class Magic_Weapon(Weapon):
    def __init__(self, tier, attack_speed, range, magic_damage, projectile_speed):
        super().__init__(tier, attack_speed, range)
        self.magic_damage = magic_damage
        self.projectile_speed = projectile_speed