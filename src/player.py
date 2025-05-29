import pygame
import math
import entity

from settings import WIDTH, HEIGHT

class Player(entity.Entity):
    def __init__(self):
        super().__init__(x = WIDTH // 2, y = HEIGHT // 2, width=100, height=100, image_path="src/sprites/player.png")
        # stats
        self.vigor = 11
        self.strength = 10
        self.dexterity = 10
        self.intelligence = 10
        self.endurance = 11
        ####
        
        self.max_hp = 3
        self.current_hp = self.max_hp
        self.hp_regen = 1 # dodac
        self.melee_dmg = 0 # dodac
        self.ranged_dmg = 0 # dodac
        self.magic_dmg = 0 # dodac
        self.damage = 2 # dodac
        self.attack_speed = 1
        self.range = 500
        self.armor = 1 # dodac
        self.speed = 3
        self.level = 1
        self.pending_level_ups = 0
        self.exp = 0
        self.exp_needed = 30
        self.gold = 0
        
        # time
        self.last_time_attack = pygame.time.get_ticks()
        self.last_time_hp_regen = pygame.time.get_ticks()
        self.last_time_damaged = pygame.time.get_ticks()
        self.last_hit_time = 0
        self.hit_cooldown = 1000

    # overrided function
    def get_rect(self):
        return pygame.Rect(self.x + 10, self.y + 10, self.width - 20, self.height - 20)
    
    def move(self, keys):
        move_x = 0
        move_y = 0

        # get input
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move_y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move_y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move_x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move_x += 1

        # set same speed diagonally
        if move_x != 0 or move_y != 0:
            length = (move_x ** 2 + move_y ** 2) ** 0.5
            move_x /= length
            move_y /= length

        self.x += move_x * self.speed
        self.y += move_y * self.speed

        # move only in screen
        self.x = max(0, min(WIDTH - self.width, self.x))
        self.y = max(0, min(HEIGHT - self.height, self.y))
        
    def take_damage(self, dmg):
        self.current_hp -= dmg
        if self.current_hp < 0:
            self.current_hp = 0
            
        now = pygame.time.get_ticks()
        self.last_time_damaged = now
        self.last_time_hp_regen = now

    def attack(self, enemies):
        # attack cooldown
        current_time = pygame.time.get_ticks()
        time_since_last_attack = (current_time - self.last_time_attack) / 1000

        # check if enemy in range
        enemies_in_range = []
        for enemy in enemies:
            if self.distance_to(enemy) <= self.range:
                enemies_in_range.append(enemy)

        # attack enemy
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
        # cooldown
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
        self.armor = upgrade_preview_stats["Armor"]
        self.speed = upgrade_preview_stats["Speed"]
        
    def reset_stats(self):
        self.max_hp = 300
        self.current_hp = self.max_hp
        self.hp_regen = 1
        self.melee_dmg = 0
        self.ranged_dmg = 0
        self.magic_dmg = 0
        self.damage = 20
        self.attack_speed = 15
        self.range = 500
        self.armor = 1
        self.speed = 3
        self.level = 1
        self.pending_level_ups = 0
        self.exp = 0
        self.exp_needed = 30
        self.gold = 0