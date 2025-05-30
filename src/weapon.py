import pygame
from projectile import *
from player import *

WEAPONS = {
    "pistol": {"damage": 3, "attack_speed": 0.5, "range": 300, "projectile_speed": 7, "sprite": "src/sprites/weapons/pistol.png"}, 
    "sword": {"damage": 5, "attack_speed": 1.5, "range": 150, "sprite": "src/sprites/weapons/sword.png"},
    "pyromancy_flame": {"damage": 5, "attack_speed": 0.5, "range": 300, "projectile_speed": 7, "sprite": "src/sprites/weapons/pyromancy_flame.png"}, 
}

class Magic_Weapon:
    def __init__(self, weapon_type):
        self.weapon_type = WEAPONS[weapon_type]
        self.damage = self.weapon_type["damage"]
        self.attack_speed = self.weapon_type["attack_speed"]
        self.range = self.weapon_type["range"]
        self.projectile_speed = self.weapon_type["projectile_speed"]
        self.image = pygame.transform.scale(pygame.image.load(self.weapon_type["sprite"]), (70, 70))
        self.last_attack_time = pygame.time.get_ticks()
        
    def attack(self, player, enemies, side=None):
        current_time = pygame.time.get_ticks()
        cooldown = int(1000 / self.attack_speed)
        if current_time - self.last_attack_time >= cooldown and enemies:
            px = player.x + player.width // 2
            py = player.y + player.height // 2

            if side == "left":
                filtered_enemies = [e for e in enemies if e.x + e.width // 2 < px]
            elif side == "right":
                filtered_enemies = [e for e in enemies if e.x + e.width // 2 >= px]
            else:
                filtered_enemies = enemies

            if not filtered_enemies:
                return None

            nearest = min(filtered_enemies, key=lambda e: ((e.x + e.width//2 - px)**2 + (e.y + e.height//2 - py)**2))
            ex = nearest.x + nearest.width // 2
            ey = nearest.y + nearest.height // 2
            dx = ex - px
            dy = ey - py

            projectile = Projectile(
                x=px - 5,
                y=py - 5,
                width=10,
                height=10,
                speed=self.projectile_speed,
                damage=self.damage,
                range=self.range,
            )
            self.last_attack_time = current_time
            return projectile
        return None
        