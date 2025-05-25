import pygame
import math

ENEMIES = {
    "zombie_cabbage": {"max_hp": 3, "speed": 1, "damage": 2, "attack_speed": 1, "range": 50, "exp": 8, "gold": 5, "sprite": "src/sprites/enemies/zombie_cabbage.png"},
    "rotten_carrot": {"max_hp": 1, "speed": 4, "damage": 1, "attack_speed": 1.5, "range": 50, "exp": 2, "gold": 2, "sprite": "src/sprites/enemies/rotten_carrot.png"},
    
}

class Enemy:
    def __init__(self, enemy_type, x, y):
        # stats
        self.enemy_type = ENEMIES[enemy_type]
        self.max_hp = self.enemy_type["max_hp"]
        self.current_hp = self.max_hp
        self.speed = self.enemy_type["speed"]
        self.damage = self.enemy_type["damage"]
        self.attack_speed = self.enemy_type["attack_speed"]
        self.range = self.enemy_type["range"]
        self.last_time_attack = pygame.time.get_ticks()

        self.x = x
        self.y = y
        self.width = 80
        self.height = 80

        self.sprite = pygame.image.load(self.enemy_type["sprite"])
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))

    def draw(self, screen):
        screen.surface.blit(self.sprite, (self.x, self.y))

    def follow_player(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)

        if distance == 0:
            return
        
        dx /= distance
        dy /= distance

        self.x += dx * self.speed
        self.y += dy * self.speed
        
    def distance_to(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        return math.hypot(dx, dy)

    def attack(self, player):
        current_time = pygame.time.get_ticks()
        time_since_last_attack = (current_time - self.last_time_attack) / 1000

        ####### dodac armor gracza!
        if self.distance_to(player) <= self.range and time_since_last_attack >= 1 / self.attack_speed:
            player.current_hp -= self.damage
            self.last_time_attack = current_time
            print(f"Enemy attacked Player for {self.damage}")
        ####### dodac armor gracza!