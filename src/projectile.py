import entity

from math import hypot

class Projectile(entity.Entity):
    def __init__(self, x, y, width, height, speed, damage, range, image_path=None):
        super().__init__(x, y, width, height)
        self.speed = speed
        self.damage = damage
        self.range = range
        self.target = None
        self.travelled = 0
        #self.image = pygame.transform.scale(pygame.image.load(image_path), (50, 50))
        
    def update(self, enemies):
        if not self.target or self.target.current_hp <= 0:
            self.target = self.find_closest_enemy(enemies)
        if self.target:
            self.follow_enemy(self.target)
            
    def should_remove(self, screen_width, screen_height):
        if (self.x < 0 or self.x > screen_width or self.y < 0 or self.y > screen_height):
            return True
        if self.travelled > self.range:
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
        dx = enemy.x - self.x
        dy = enemy.y - self.y
        distance = hypot(dx, dy)
        if distance == 0:
            return
        dx /= distance
        dy /= distance
        self.x += dx * self.speed
        self.y += dy * self.speed
        
    def distance_to(self, enemy):
        dx = self.x - enemy.x
        dy = self.y - enemy.y
        return hypot(dx, dy)