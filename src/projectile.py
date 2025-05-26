from math import hypot

class Projectile:
    def __init__(self, weapon, speed, damage):
        self.x = weapon.x
        self.y = weapon.y
        self.speed = speed
        self.damage = damage
        
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
        
        
        