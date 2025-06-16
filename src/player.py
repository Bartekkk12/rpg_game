import pygame
import math
import entity

from settings import WIDTH, HEIGHT

class Player(entity.Entity):
    '''Class representing the player character.'''
    def __init__(self):
        super().__init__(x=WIDTH // 2, y=HEIGHT // 2, width=100, height=100, image_path="src/sprites/player.png")
        self.max_hp = 10
        self.current_hp = self.max_hp
        self.hp_regen = 1
        self.melee_dmg = 1
        self.ranged_dmg = 1
        self.magic_dmg = 1
        self.max_armor = 5
        self.current_armor = self.max_armor
        self.speed = 3
        self.level = 1
        self.pending_level_ups = 0
        self.exp = 0
        self.exp_needed = 30
        self.gold = 0 

        # weapons
        self.weapons = {}
        self.MAX_WEAPONS = 4
        self.current_weapons = 0

        # timers
        self.last_time_attack = pygame.time.get_ticks()
        self.last_time_hp_regen = pygame.time.get_ticks()
        self.last_time_damaged = pygame.time.get_ticks()
        self.last_hit_time = 0
        self.hit_cooldown = 1000

    def get_rect(self):
        '''Returns a reduced hitbox for the player.'''
        return pygame.Rect(self.x + 10, self.y + 10, self.width - 20, self.height - 20)

    def move(self, keys):
        '''Handles movement input and moves player accordingly.'''
        move_x = 0
        move_y = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move_y -= 1
            self.image = pygame.transform.flip(self.fliped_image, True, False)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move_y += 1
            self.image = pygame.transform.flip(self.fliped_image, True, False)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move_x -= 1
            self.image = self.fliped_image
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move_x += 1
            self.image = pygame.transform.flip(self.fliped_image, True, False)

        if move_x != 0 or move_y != 0:
            length = math.hypot(move_x, move_y)
            move_x /= length
            move_y /= length

        self.x += move_x * self.speed
        self.y += move_y * self.speed

        # Clmap position within screen bounds
        self.x = max(0, min(WIDTH - self.width, self.x))
        self.y = max(0, min(HEIGHT - self.height, self.y))
        
    def take_damage(self, dmg):
        '''Applies damage to player, first to armor, then to HP. Resets regen timers.'''
        if self.current_armor > 0:
            absorbed = min(dmg, self.current_armor)
            self.current_armor -= absorbed
            dmg -= absorbed

        self.current_hp -= dmg
        self.current_hp = max(self.current_hp, 0)
            
        now = pygame.time.get_ticks()
        self.last_time_damaged = now
        self.last_time_hp_regen = now
    
    def regen_hp(self):
        '''Regenerates HP if enough time has passed since last damage and last regen.'''
        current_time = pygame.time.get_ticks()
        time_since_last_damage = (current_time - self.last_time_damaged) / 1000
        time_since_last_regen = (current_time - self.last_time_hp_regen) / 1000

        if self.hp_regen > 0 and self.current_hp < self.max_hp and time_since_last_damage >= 2 and time_since_last_regen >= 2:
            self.current_hp += self.hp_regen
            if self.current_hp > self.max_hp:
                self.current_hp = self.max_hp
            self.last_time_hp_regen = current_time
            print(f"Player hp regened for {self.hp_regen}")
            
    def check_level_up(self):
        '''Checks if the player has enough experience to level up.'''
        return self.exp >= self.exp_needed
    
    def level_up(self):
        '''Levbels up the player, increases stats, and sets experience for next level.'''
        self.level += 1
        self.max_hp += 1
        self.pending_level_ups += 3
        self.exp -= self.exp_needed
        self.exp_needed += 20
        
    def apply_upgrades(self, upgrade_preview_stats):
        '''Applies new stats from upgrade preview.'''
        self.max_hp = upgrade_preview_stats["HP"]
        self.melee_dmg = upgrade_preview_stats["Melee Damage"]
        self.ranged_dmg = upgrade_preview_stats["Ranged Damage"]
        self.magic_dmg = upgrade_preview_stats["Magic Damage"]
        self.max_armor = upgrade_preview_stats["Armor"]
        self.speed = upgrade_preview_stats["Speed"]

    @staticmethod
    def filter_enemies_by_side(weapon_x, enemies, side):
        '''Filters enemies by their position relative to a weapon (left/right)'''
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
        '''Calculates the angle from weapon position to the nearest enemy, considering side.'''
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
        '''Clamps the weapon's angle to stay on its side (left/right).'''
        angle = (angle + 360) % 360
        if side == "right":
            if 90 < angle < 270:
                angle = 90 if angle < 180 else 270
        elif side == "left":
            if angle < 90 or angle > 270:
                angle = 90 if angle < 180 else 270
        return angle
            
    def draw_weapons(self, screen, enemies=None):
        '''Draws all of the player's weapons, rotated towards nearest enemy.'''
        weapon_size = 70
        spacing = 10
        cx = self.x + self.width // 2
        cy = self.y + self.height // 2

        offsets = []
        sides = []
        weapon_objs = list(self.weapons.values())
        if len(weapon_objs) == 1:
            offsets = [(0, -weapon_size//2 - spacing)]
            sides = ["center"]
        elif len(weapon_objs) == 2:
            offsets = [(-weapon_size//2 - spacing, -weapon_size//3),
                       (weapon_size//2 + spacing, -weapon_size//3)]
            sides = ["left", "right"]
        elif len(weapon_objs) == 3:
            offsets = [(-weapon_size//2 - spacing, 0),
                       (weapon_size//2 + spacing, 0),
                       (0, -weapon_size//2 - spacing)]
            sides = ["left", "right", "left"]
        elif len(weapon_objs) == 4:
            offsets = [(-weapon_size//2 - spacing, -weapon_size//3),
                       (weapon_size//2 + spacing, -weapon_size//3),
                       (-weapon_size//2 - spacing, weapon_size//3),
                       (weapon_size//2 + spacing, weapon_size//3)]
            sides = ["left", "right", "left", "right"]

        for weapon, (ox, oy), side in zip(weapon_objs, offsets, sides):
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
        '''Resets all player stats to their starting values.'''
        self.max_hp = 10
        self.current_hp = self.max_hp
        self.hp_regen = 1
        self.melee_dmg = 1
        self.ranged_dmg = 1
        self.magic_dmg = 1
        self.max_armor = 5
        self.current_armor = self.max_armor
        self.speed = 3
        self.level = 1
        self.pending_level_ups = 0
        self.exp = 0
        self.exp_needed = 30
        self.gold = 0 