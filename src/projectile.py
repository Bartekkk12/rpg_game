import entity
import pygame

from math import hypot, atan2, degrees
from assets import get_projectile_image

class Projectile(entity.Entity):
    def __init__(self, x, y, width, height, speed, damage, range, image_path, direction=None, homing=False, target_pos=None, side="center"):
        super().__init__(x, y, width, height, image_path)
        self.speed = speed
        self.damage = damage
        self.range = range
        self.homing = homing
        self.target = None # Only for homing
        self.target_pos = target_pos  # Only for straight
        self.travelled = 0
        self.direction = direction
        self.last_direction = direction
        self.lost_target = False
        self.side = side
        self.base_image = get_projectile_image(image_path, (width, height))

    def update(self, enemies):
        if self.homing and not self.lost_target:
            if self.target is None or getattr(self.target, "current_hp", 1) <= 0:
                if self.target is not None:
                    self.lost_target = True
                else:
                    self.target = self.find_closest_enemy(enemies)
            if self.target is not None and getattr(self.target, "current_hp", 1) > 0:
                dx = (self.target.x + self.target.width//2) - (self.x + self.width//2)
                dy = (self.target.y + self.target.height//2) - (self.y + self.height//2)
                distance = hypot(dx, dy)
                if distance != 0:
                    dx /= distance
                    dy /= distance
                    self.last_direction = (dx, dy)
                    self.x += dx * self.speed
                    self.y += dy * self.speed
                    self.travelled += self.speed
            elif self.lost_target and self.last_direction is not None:
                self.x += self.last_direction[0] * self.speed
                self.y += self.last_direction[1] * self.speed
                self.travelled += self.speed
        elif self.homing and self.lost_target:
            if self.last_direction is not None:
                self.x += self.last_direction[0] * self.speed
                self.y += self.last_direction[1] * self.speed
                self.travelled += self.speed
        else:
            if self.direction is not None:
                self.x += self.direction[0] * self.speed
                self.y += self.direction[1] * self.speed
                self.travelled += self.speed
            
    def should_remove(self, screen_width, screen_height):
        return (self.x < 0 or self.x > screen_width or self.y < 0 or self.y > screen_height)
        
    def find_closest_enemy(self, enemies):
        px = self.x + self.width // 2
        if self.side == "left":
            filtered = [e for e in enemies if e.x + e.width // 2 < px and getattr(e, "current_hp", 1) > 0]
        elif self.side == "right":
            filtered = [e for e in enemies if e.x + e.width // 2 >= px and getattr(e, "current_hp", 1) > 0]
        else:
            filtered = [e for e in enemies if getattr(e, "current_hp", 1) > 0]
        if not filtered:
            filtered = [e for e in enemies if getattr(e, "current_hp", 1) > 0]
        if not filtered:
            return None
        return min(filtered, key=lambda enemy: self.distance_to(enemy))
        
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
    
    def draw(self, screen):
        direction = self.last_direction if self.homing else self.direction
        if direction is not None and direction != (0, 0):
            angle_rad = atan2(-direction[1], direction[0])
            angle_deg = degrees(angle_rad)
        else:
            angle_deg = 0
        rotated_image = pygame.transform.rotate(self.base_image, angle_deg)
        rotated_rect = rotated_image.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.surface.blit(rotated_image, rotated_rect)