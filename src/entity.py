import pygame

class Entity:
    def __init__(self, x, y, width, height, image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(pygame.image.load(image_path), (width, height)) if image_path else None
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        screen.surface.blit(self.image, (self.x, self.y))
            
    def draw_hit_box(self, screen, color):
        pygame.draw.rect(screen.surface, color, self.get_rect(), 2)