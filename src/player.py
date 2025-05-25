import pygame
import math
from settings import WIDTH, HEIGHT

class Player:
    def __init__(self, name):
        # stats
        self._name = name
        self.max_hp = 1
        self.current_hp = self.max_hp
        self.hp_regen = 0 # dodac
        self.melee_dmg = 0 # dodac
        self.ranged_dmg = 0 # dodac
        self.magic_dmg = 0 # dodac
        self.damage = 2 # dodac
        self.attack_speed = 1
        self.range = 500
        self.armor = 1 # dodac
        self.speed = 10
        self.level = 1
        self.pending_level_ups = 0
        self.exp = 0
        self.exp_needed = 30
        self.gold = 0
        self.last_time_attack = pygame.time.get_ticks()

        # sprite and position
        self.width = 100
        self.height = 100
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.sprite = pygame.image.load("src/sprites/player.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))

    def draw(self, screen):
        screen.surface.blit(self.sprite, (self.x, self.y))

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
    
    def level_up(self):
        self.level += 1
        self.pending_level_ups += 3
        self.exp -= self.exp_needed
        self.exp_needed += 20
        
    def reset_stats(self):
        self.max_hp = 3
        self.current_hp = self.max_hp
        self.hp_regen = 0
        self.melee_dmg = 0
        self.ranged_dmg = 0
        self.magic_dmg = 0
        self.damage = 2
        self.attack_speed = 1
        self.range = 500
        self.armor = 1
        self.speed = 3
        self.level = 1
        self.pending_level_ups = 0
        self.exp = 0
        self.exp_needed = 30
        self.gold = 0