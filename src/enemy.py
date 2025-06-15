import pygame
import math
import entity

ENEMIES = {
    # first wave appearing 1
    "zombie_cabbage": {"max_hp": 5, "speed": 3, "damage": 1, "attack_speed": 1, "range": 50, "exp": 1, "gold": 1, "sprite": "src/sprites/enemies/zombie_cabbage.png", "size": 80,
                       "hp+/wave": 2, "dmg+/wave": 1, "spawn_wave": 1},
    
    # first wave appearing 1
    "rotten_carrot": {"max_hp": 2, "speed": 9, "damage": 1, "attack_speed": 1, "range": 50, "exp": 1, "gold": 1, "sprite": "src/sprites/enemies/rotten_carrot.png", "size": 80,
                      "hp+/wave": 1, "dmg+/wave": 1, "spawn_wave": 1},
                          
    # first wave appearing 2
    "vampire_garlic": {"max_hp": 6, "speed": 3, "damage": 2, "attack_speed": 1, "range": 50, "exp": 4, "gold": 4, "sprite": "src/sprites/enemies/vampire_garlic.png", "size": 80,
                       "hp+/wave": 2, "dmg+/wave": 1, "spawn_wave": 2},
    
    # first wave appearing 4
    "mad_mushroom": {"max_hp": 8, "speed": 3, "damage": 2, "attack_speed": 1, "range": 50, "exp": 2, "gold": 2, "sprite": "src/sprites/enemies/mad_mushroom.png", "size": 80,
                     "hp+/wave": 1, "dmg+/wave": 1, "spawn_wave": 4},
    
    # first wave appearing 6
    "mutan_broccoli": {"max_hp": 15, "speed": 3, "damage": 5, "attack_speed": 1, "range": 50, "exp": 10, "gold": 10, "sprite": "src/sprites/enemies/mutant_broccoli.png", "size": 80,
                       "hp+/wave": 5, "dmg+/wave": 1, "spawn_wave": 6},
    
    # first wave appearing 8
    "angry_tomato": {"max_hp": 30, "speed": 4, "damage": 7, "attack_speed": 1, "range": 50, "exp": 20, "gold": 15, "sprite": "src/sprites/enemies/angry_tomato.png", "size": 80,
                       "hp+/wave": 5, "dmg+/wave": 1, "spawn_wave": 6},
    
    # first wave appearing 20
    #"onion_boss": {"max_hp": 150, "speed": 5, "damage": 15, "attack_speed": 1, "range": 100, "exp": 100, "gold": 100, "sprite": "src/sprites/enemies/onion_boss.png", "size": 150},
}

class Enemy(entity.Entity):
    def __init__(self, enemy_type, x, y, current_round):
        super().__init__(x, y, ENEMIES[enemy_type]["size"], ENEMIES[enemy_type]["size"], ENEMIES[enemy_type]["sprite"])
        # stats
        self.enemy_type = ENEMIES[enemy_type]
        self.max_hp = self.enemy_type["max_hp"] + self.enemy_type["hp+/wave"] * max(0, current_round - self.enemy_type["spawn_wave"])
        self.current_hp = self.max_hp
        self.speed = self.enemy_type["speed"]
        self.damage = self.enemy_type["damage"] + self.enemy_type["dmg+/wave"] * max(0, current_round - self.enemy_type["spawn_wave"])
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
