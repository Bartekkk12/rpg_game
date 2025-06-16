import pygame

from assets import *
from math import hypot

class Entity:
    '''Base class representing any entity (player, enemy, etc.) in the game'''
    def __init__(self, x, y, width, height, image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = get_sprite(image_path, (width, height))
        self.fliped_image = pygame.transform.flip(self.image, True, False)
        
    def get_rect(self):
        '''Returns a rectangle for the entity, used for collision and drawing'''
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        '''Draws the entity sprite on the screen'''
        screen.surface.blit(self.image, (self.x, self.y))
            
    def draw_hit_box(self, screen, color):
        '''Draws the entity's hitbox for debugging purposes.'''
        pygame.draw.rect(screen.surface, color, self.get_rect(), 2)
        
    def distance_to(self, other):
        '''Returns the Euclidean distance to an enemy.'''
        dx = self.x - other.x
        dy = self.y - other.y
        return hypot(dx, dy)
        