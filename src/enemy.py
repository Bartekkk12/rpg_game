import pygame
import math
import entity

ENEMIES = {
    "zombie_cabbage": {"max_hp": 3, "speed": 3, "damage": 2, "attack_speed": 1, "range": 50, "exp": 8, "gold": 5, "sprite": "src/sprites/enemies/zombie_cabbage.png"},
    "rotten_carrot": {"max_hp": 1, "speed": 5, "damage": 1, "attack_speed": 1.5, "range": 50, "exp": 2, "gold": 2, "sprite": "src/sprites/enemies/rotten_carrot.png"},
    "vampire_garlic": {"max_hp": 5, "speed": 3, "damage": 2, "attack_speed": 1, "range": 50, "exp": 10, "gold": 15, "sprite": "src/sprites/enemies/vampire_garlic.png"},
    "mutan_broccoli": {"max_hp": 10, "speed": 2, "damage": 5, "attack_speed": 0.7, "range": 50, "exp": 35, "gold": 20, "sprite": "src/sprites/enemies/mutant_broccoli.png"},
    "mad_mushroom": {"max_hp": 4, "speed": 3, "damage": 3, "attack_speed": 1.5, "range": 50, "exp": 20, "gold": 10, "sprite": "src/sprites/enemies/mad_mushroom.png"},
    #"onion_boss": {"max_hp": 150, "speed": 5, "damage": 15, "attack_speed": 1.5, "range": 100, "exp": 100, "gold": 100, "sprite": "src/sprites/enemies/onion_boss.png"},
}

class Enemy(entity.Entity):
    def __init__(self, enemy_type, x, y):
        super().__init__(x, y, 80, 80, ENEMIES[enemy_type]["sprite"])
        # stats
        self.enemy_type = ENEMIES[enemy_type]
        self.max_hp = self.enemy_type["max_hp"]
        self.current_hp = self.max_hp
        self.speed = self.enemy_type["speed"]
        self.damage = self.enemy_type["damage"]
        self.attack_speed = self.enemy_type["attack_speed"]
        self.range = self.enemy_type["range"]
        self.last_time_attack = pygame.time.get_ticks()
        self.direction = ""

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        
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
        
        self.rect.topleft = (self.x, self.y)
        
    def distance_to(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        return math.hypot(dx, dy)

    def attack(self, player):
        current_time = pygame.time.get_ticks()
        time_since_last_attack = (current_time - self.last_time_attack) / 1000
        
        # attack enemy if collide
        now = pygame.time.get_ticks()
        if self.rect.colliderect(player.get_rect()):
            if now - player.last_hit_time >= player.hit_cooldown:
                player.take_damage(self.damage)
                player.last_hit_time = now
                print(f"Player collide with enemy for {self.damage} dmg")

        # attack player if in range
        if self.distance_to(player) <= self.range and time_since_last_attack >= 1 / self.attack_speed:
            player.take_damage(self.damage)
            self.last_time_attack = current_time
            print(f"Enemy attacked Player for {self.damage} dmg")
