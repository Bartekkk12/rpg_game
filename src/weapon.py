import pygame
from projectile import *
from player import *

WEAPONS = {
    "pistol": {"level": 1, "damage": 1, "attack_speed": 1.5, "range": 300, "projectile_speed": 20, "sprite": "src/sprites/weapons/pistol.png", "sound": "src/sprites/sounds/pistol_shot_sound.wav", "sound_volume": 0.1, "projectile": "src/sprites/weapons/bullet.png",
               "damage/upgrade": 1, "attack_speed/upgrade": 0.3, "projectile_speed/upgrade": 2},
    
    "bow": {"level": 1, "damage": 3, "attack_speed": 0.5, "range": 300, "projectile_speed": 20, "sprite": "src/sprites/weapons/bow.png", "sound": "src/sprites/sounds/bow_release.wav", "sound_volume": 0.5, "projectile": "src/sprites/weapons/arrow.png",
               "damage/upgrade": 1.5, "attack_speed/upgrade": 0.1, "projectile_speed/upgrade": 3},
     
    "sword": {"level": 1, "damage": 4, "attack_speed": 1, "range": 150, "sprite": "src/sprites/weapons/sword.png", "sound": "src/sprites/sounds/scythe_slash.wav", "sound_volume": 4,
              "damage/upgrade": 1.5, "attack_speed/upgrade": 0.1, "range/upgrade": 15},
    
    "scythe": {"level": 1, "damage": 6, "attack_speed": 0.5, "range": 200, "sprite": "src/sprites/weapons/scythe.png", "sound": "src/sprites/sounds/scythe_slash.wav", "sound_volume": 4,
               "damage/upgrade": 2.2, "attack_speed/upgrade": 0.1, "range/upgrade": 15},
    
    "pyromancy_flame": {"damage": 2.5, "attack_speed": 0.5, "range": 300, "projectile_speed": 7, "sprite": "src/sprites/weapons/pyromancy_flame.png", "sound": "src/sprites/sounds/fire_ball_sound.wav", "sound_volume": 0.1, "projectile": "src/sprites/weapons/fire_ball.png",
               "damage/upgrade": 1.1, "attack_speed/upgrade": 0.2, "range/upgrade": 15},
    
    "magic_wand": {"damage": 1, "attack_speed": 1.5, "range": 300, "projectile_speed": 7, "sprite": "src/sprites/weapons/magic_wand.png", "sound": "src/sprites/sounds/fire_ball_sound.wav", "sound_volume": 0.1, "projectile": "src/sprites/weapons/magic_bullet.png",
                   "damage/upgrade": 1, "attack_speed/upgrade": 0.3, "range/upgrade": 15}, 
}

class Weapon:
    def __init__(self, weapon_type):
        self.weapon_name = weapon_type
        self.weapon_type = WEAPONS[weapon_type]
        self.attack_speed = self.weapon_type["attack_speed"]
        self.range = self.weapon_type["range"]
        self.image = pygame.transform.scale(pygame.image.load(self.weapon_type["sprite"]), (70, 70))
        self.sound = pygame.mixer.Sound(self.weapon_type.get("sound", ""))
        self.sound.set_volume(self.weapon_type["sound_volume"])
        self.last_attack_time = pygame.time.get_ticks()
        
    def play_sound(self):
        if self.sound:
            self.sound.play()
            
class Melee_Weapon(Weapon):
    def __init__(self, weapon_type):
        super().__init__(weapon_type)
        
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

            if filtered_enemies:
                target_list = filtered_enemies
            else:
                target_list = enemies

            if not target_list:
                return None 
                
            nearest = min(target_list, key=lambda e: ((e.x + e.width//2 - px)**2 + (e.y + e.height//2 - py)**2))
            ex = nearest.x + nearest.width // 2
            ey = nearest.y + nearest.height
            dist = ((ex - px)**2 + (ey - py)**2) ** 0.5
                
            if dist <= self.range:
                self.damage = self.weapon_type["damage"] + player.melee_dmg
                nearest.current_hp -= self.damage
                print(f"Melee Weapon hit enemy for {self.damage}")
                self.play_sound()
                
            self.last_attack_time = current_time


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

            if filtered_enemies:
                target_list = filtered_enemies
            else:
                target_list = enemies

            if not target_list:
                return None 

            nearest = min(target_list, key=lambda e: ((e.x + e.width//2 - px)**2 + (e.y + e.height//2 - py)**2))
            ex = nearest.x + nearest.width // 2
            ey = nearest.y + nearest.height // 2
            dx = ex - px
            dy = ey - py
            dist = (dx ** 2 + dy ** 2) ** 0.5
            direction = (dx / dist, dy / dist) if dist != 0 else (0, 0)
            
            # change projectile size
            width = 50 if self.weapon_name == "bow" else 10
            height = 50 if self.weapon_name == "bow" else 10

            self.damage = self.weapon_type["damage"] + player.ranged_dmg
            projectile = Projectile(
                x=px - 5, y=py - 5, width=width, height=height,
                speed=self.projectile_speed, damage=self.damage,
                range=self.range, image_path=self.projectile_image,
                direction=direction, homing=False, side=side
                )
            self.last_attack_time = current_time
            self.play_sound()
            
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
        if current_time - self.last_attack_time < cooldown or not enemies:
            return None
        
        px = player.x + player.width // 2
        py = player.y + player.height // 2

        if side == "left":
            filtered_enemies = [e for e in enemies if e.x + e.width // 2 < px]
        elif side == "right":
            filtered_enemies = [e for e in enemies if e.x + e.width // 2 >= px]
        else:
            filtered_enemies = enemies

        if filtered_enemies:
            target_list = filtered_enemies
        else:
            target_list = enemies

        if not target_list:
            return None 

        self.damage = self.weapon_type["damage"] + player.magic_dmg
        projectile = Projectile(
            x=px - 5, y=py - 5, width=40, height=40,
            speed=self.projectile_speed, damage=self.damage,
            range=self.range, image_path=self.projectile_image,
            direction=None, homing=True, side=side
        )
        self.last_attack_time = current_time
        self.play_sound()
        return projectile