import pygame
import entity

class Gold(entity.Entity):
    def __init__(self, x, y, amount, exp):
        super().__init__(x, y, width=50, height=50, image_path="src/sprites/gold_exp.png")
        self.amount = amount
        self.exp = exp
        self.gold_pickup_sound = pygame.mixer.Sound("src/sprites/sounds/pop_sound.wav")
        self.gold_pickup_sound.set_volume(0.2)
        
    def play_sound(self):
        self.gold_pickup_sound.play()