import pygame
from projectile import *
from player import *

WEAPONS = {
    "pistol": {"damage": 1, "attack_speed": 1.5, "range": 300, "projectile_speed": 20, "sprite": "src/sprites/weapons/pistol.png", "sound": "src/sprites/sounds/pistol_shot_sound.wav", "projectile": "src/sprites/weapons/bullet.png"}, 
    "sword": {"damage": 5, "attack_speed": 1.5, "range": 150, "sprite": "src/sprites/weapons/sword.png"},
    "pyromancy_flame": {"damage": 5, "attack_speed": 0.5, "range": 300, "projectile_speed": 7, "sprite": "src/sprites/weapons/pyromancy_flame.png", "sound": "src/sprites/sounds/fire_ball_sound.wav", "projectile": "src/sprites/weapons/fire_ball.png"}, 
    "magic_wand": {"damage": 10, "attack_speed": 0.5, "range": 300, "projectile_speed": 7, "sprite": "src/sprites/weapons/magic_wand.png", "sound": "src/sprites/sounds/fire_ball_sound.wav", "projectile": "src/sprites/weapons/magic_bullet.png"}, 

}

class Weapon:
    def __init__(self, weapon_type):
        self.weapon_type = WEAPONS[weapon_type]
        self.damage = self.weapon_type["damage"]
        self.attack_speed = self.weapon_type["attack_speed"]
        self.range = self.weapon_type["range"]
        self.image = pygame.transform.scale(pygame.image.load(self.weapon_type["sprite"]), (70, 70))
        self.sound = pygame.mixer.Sound(self.weapon_type.get("sound", ""))
        self.sound.set_volume(0.1)
        self.last_attack_time = pygame.time.get_ticks()
        
    def play_sound(self):
        if self.sound:
            self.sound.play()

class Ranged_Weapon(Weapon):
    def __init__(self, weapon_type):
        super().__init__(weapon_type)
        self.projectile_speed = self.weapon_type["projectile_speed"]
        self.projectile_image = self.weapon_type["projectile"]

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

            target_list = filtered_enemies if filtered_enemies else enemies

            if not target_list:
                return None

            nearest = min(target_list, key=lambda e: ((e.x + e.width//2 - px)**2 + (e.y + e.height//2 - py)**2))
            ex = nearest.x + nearest.width // 2
            ey = nearest.y + nearest.height // 2
            dx = ex - px
            dy = ey - py
            dist = (dx ** 2 + dy ** 2) ** 0.5
            direction = (dx / dist, dy / dist) if dist != 0 else (0, 0)

            self.play_sound()
            projectile = Projectile(x=px - 5, y=py - 5, width=10, height=10, speed=self.projectile_speed, damage=self.damage, range=self.range, image_path=self.projectile_image, direction=direction, homing=False)
            self.last_attack_time = current_time
            
            return projectile
        return None

class Magic_Weapon(Weapon):
    def __init__(self, weapon_type):
        super().__init__(weapon_type)
        self.projectile_speed = self.weapon_type["projectile_speed"]
        self.projectile_image = self.weapon_type["projectile"]

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

            target_list = filtered_enemies if filtered_enemies else enemies

            if not target_list:
                return None

            nearest = min(target_list, key=lambda e: ((e.x + e.width//2 - px)**2 + (e.y + e.height//2 - py)**2))

            self.play_sound()

            projectile = Projectile(x=px - 5, y=py - 5, width=40, height=40, speed=self.projectile_speed, damage=self.damage, range=self.range, image_path=self.projectile_image, direction=None, homing=True)
            self.last_attack_time = current_time
            
            return projectile
        return None