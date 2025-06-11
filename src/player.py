import pygame
import math
import entity

from settings import WIDTH, HEIGHT

class Player(entity.Entity):
    def __init__(self):
        super().__init__(x=WIDTH // 2, y=HEIGHT // 2, width=100, height=100, image_path="src/sprites/player.png")
        self.max_hp = 3
        self.current_hp = self.max_hp
        self.hp_regen = 1
        self.melee_dmg = 0
        self.ranged_dmg = 0
        self.magic_dmg = 0
        self.attack_speed = 1
        self.range = 500
        self.max_armor = 1
        self.current_armor = self.max_armor
        self.speed = 3
        self.level = 1
        self.pending_level_ups = 0
        self.exp = 0
        self.exp_needed = 30
        self.gold = 0
        
        # weapons
        self.weapons = []
        self.MAX_WEAPONS = 4
        self.current_weapons = 0
        
        # time
        self.last_time_attack = pygame.time.get_ticks()
        self.last_time_hp_regen = pygame.time.get_ticks()
        self.last_time_damaged = pygame.time.get_ticks()
        self.last_hit_time = 0
        self.hit_cooldown = 1000

    def get_rect(self):
        return pygame.Rect(self.x + 10, self.y + 10, self.width - 20, self.height - 20)

    def move(self, keys):
        move_x = 0
        move_y = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move_y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move_y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move_x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move_x += 1

        if move_x != 0 or move_y != 0:
            length = (move_x ** 2 + move_y ** 2) ** 0.5
            move_x /= length
            move_y /= length

        self.x += move_x * self.speed
        self.y += move_y * self.speed

        self.x = max(0, min(WIDTH - self.width, self.x))
        self.y = max(0, min(HEIGHT - self.height, self.y))
        
    def take_damage(self, dmg):
        if self.current_armor > 0:
            self.current_armor -= dmg
        else: 
            self.current_armor = 0
            self.current_hp -= dmg
        if self.current_hp < 0:
            self.current_hp = 0
            
        now = pygame.time.get_ticks()
        self.last_time_damaged = now
        self.last_time_hp_regen = now

    def attack(self, enemies):
        current_time = pygame.time.get_ticks()
        time_since_last_attack = (current_time - self.last_time_attack) / 1000

        enemies_in_range = []
        for enemy in enemies:
            if self.distance_to(enemy) <= self.range:
                enemies_in_range.append(enemy)

        if enemies_in_range and time_since_last_attack >= 1 / self.attack_speed:
            closest_enemy = min(enemies_in_range, key=lambda enemy: self.distance_to(enemy))
            closest_enemy.current_hp -= self.damage
            self.last_time_attack = current_time
            print(f"Player attacked Enemy for {self.damage}")

    def distance_to(self, enemy):
        dx = self.x - enemy.x
        dy = self.y - enemy.y
        return math.hypot(dx, dy)
    
    def check_level_up(self):
        return self.exp >= self.exp_needed
    
    def regen_hp(self):
        current_time = pygame.time.get_ticks()
        time_since_last_damage = (current_time - self.last_time_damaged) / 1000
        time_since_last_regen = (current_time - self.last_time_hp_regen) / 1000

        if self.hp_regen > 0 and self.current_hp < self.max_hp and time_since_last_damage >= 5 and time_since_last_regen >= 5:
            self.current_hp += 1
            if self.current_hp > self.max_hp:
                self.current_hp = self.max_hp
            self.last_time_hp_regen = current_time
            print("Player hp regened for 1")
    
    def level_up(self):
        self.level += 1
        self.pending_level_ups += 3
        self.exp -= self.exp_needed
        self.exp_needed += 20
        
    def apply_upgrades(self, upgrade_preview_stats):
        self.max_hp = upgrade_preview_stats["HP"]
        self.melee_dmg = upgrade_preview_stats["Melee Damage"]
        self.ranged_dmg = upgrade_preview_stats["Ranged Damage"]
        self.magic_dmg = upgrade_preview_stats["Magic Damage"]
        self.attack_speed = upgrade_preview_stats["Attack Speed"]
        self.range = upgrade_preview_stats["Range"]
        self.max_armor = upgrade_preview_stats["Armor"]
        self.speed = upgrade_preview_stats["Speed"]

    @staticmethod
    def filter_enemies_by_side(weapon_x, enemies, side):
        filtered = []
        for e in enemies:
            ex = e.x + e.width // 2
            dx = ex - weapon_x
            if side == "left" and dx < 0:
                filtered.append(e)
            elif side == "right" and dx > 0:
                filtered.append(e)
        return filtered

    @staticmethod
    def get_angle_to_enemy(weapon_x, weapon_y, enemies, side="center"):
        filtered_enemies = Player.filter_enemies_by_side(weapon_x, enemies, side) if side in ("left", "right") else enemies
        target_list = filtered_enemies if filtered_enemies else enemies

        if not target_list:
            return 0
        
        nearest = min(target_list, key=lambda e: (e.x + e.width//2 - weapon_x)**2 + (e.y + e.height//2 - weapon_y)**2)
        dx = (nearest.x + nearest.width//2) - weapon_x
        dy = (nearest.y + nearest.height//2) - weapon_y
        angle = math.degrees(math.atan2(-dy, dx))
        return angle
    
    @staticmethod
    def clamp_angle(angle, side):
        angle = (angle + 360) % 360
        if side == "right":
            if 90 < angle < 270:
                angle = 90 if angle < 180 else 270
        elif side == "left":
            if angle < 90 or angle > 270:
                angle = 90 if angle < 180 else 270
        return angle
            
    def draw_weapons(self, screen, enemies=None):
        weapon_size = 70
        spacing = 10
        cx = self.x + self.width // 2
        cy = self.y + self.height // 2

        offsets = []
        sides = []
        if len(self.weapons) == 1:
            offsets = [(0, -weapon_size//2 - spacing)]
            sides = ["center"]
        elif len(self.weapons) == 2:
            offsets = [(-weapon_size//2 - spacing, -weapon_size//3),
                    (weapon_size//2 + spacing, -weapon_size//3)]
            sides = ["left", "right"]
        elif len(self.weapons) == 3:
            offsets = [(-weapon_size//2 - spacing, 0),
                    (weapon_size//2 + spacing, 0),
                    (0, -weapon_size//2 - spacing)]
            sides = ["left", "right", "left"]
        elif len(self.weapons) == 4:
            offsets = [(-weapon_size//2 - spacing, -weapon_size//3),
                    (weapon_size//2 + spacing, -weapon_size//3),
                    (-weapon_size//2 - spacing, weapon_size//3),
                    (weapon_size//2 + spacing, weapon_size//3)]
            sides = ["left", "right", "left", "right"]

        for weapon, (ox, oy), side in zip(self.weapons, offsets, sides):
            wx = cx + ox - weapon_size//2
            wy = cy + oy - weapon_size//2
            angle = 0
            if enemies is not None and len(enemies) > 0:
                angle = self.get_angle_to_enemy(wx + weapon_size//2, wy + weapon_size//2, enemies, side)
                angle = self.clamp_angle(angle, side)
            weapon_img = weapon.image
            rotated_image = pygame.transform.rotate(weapon_img, angle)
            if side == "left":
                rotated_image = pygame.transform.flip(rotated_image, True, False)
            rotated_rect = rotated_image.get_rect(center=(wx + weapon_size//2, wy + weapon_size//2))
            screen.surface.blit(rotated_image, rotated_rect.topleft)

    def reset_stats(self):
        self.max_hp = 3
        self.current_hp = self.max_hp
        self.hp_regen = 1
        self.melee_dmg = 0
        self.ranged_dmg = 0
        self.magic_dmg = 0
        self.attack_speed = 1
        self.range = 50
        self.max_armor = 4
        self.current_armor = self.max_armor
        self.speed = 3
        self.level = 1
        self.pending_level_ups = 0
        self.exp = 0
        self.exp_needed = 30
        self.gold = 0 