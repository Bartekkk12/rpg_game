import entity
import pygame
from math import hypot

class Projectile(entity.Entity):
    def __init__(self, x, y, width, height, speed, damage, range, image_path, direction=None, homing=False, target_pos=None):
        super().__init__(x, y, width, height, image_path)
        self.speed = speed
        self.damage = damage
        self.range = range
        self.homing = homing
        self.target = None # Only for homing
        self.target_pos = target_pos  # Only for straight
        self.travelled = 0
        self.direction = direction
        
    def update(self, enemies):
        if self.homing:
            if not self.target or self.target.current_hp < 0:
                self.target = self.find_closest_enemy(enemies)
            if self.target:
                self.follow_enemy(self.target)
        else:
            if self.direction is not None:
                self.x += self.direction[0] * self.speed
                self.y += self.direction[1] * self.speed
                self.travelled += self.speed
            
    def should_remove(self, screen_width, screen_height):
        if (self.x < 0 or self.x > screen_width or self.y < 0 or self.y > screen_height):
            return True
        
        if self.homing and (self.target is None):
            return True
        return False
        
    def find_closest_enemy(self, enemies):
        enemies_in_range = []
        for enemy in enemies: 
            if self.distance_to(enemy) <= self.range:
                enemies_in_range.append(enemy)
        if not enemies_in_range:
            return None
        return min(enemies_in_range, key=lambda enemy: self.distance_to(enemy))
        
    def follow_enemy(self, enemy):
        dx = (enemy.x + enemy.width//2) - (self.x + self.width//2)
        dy = (enemy.y + enemy.height//2) - (self.y + self.height//2)
        distance = hypot(dx, dy)
        
        if distance == 0:
            return
        
        dx /= distance
        dy /= distance
        
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.travelled += self.speed
        
    def distance_to(self, enemy):
        dx = (self.x + self.width//2) - (enemy.x + enemy.width//2)
        dy = (self.y + self.height//2) - (enemy.y + enemy.height//2)
        return hypot(dx, dy)