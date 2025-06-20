import pygame

LOADED_SPRITES = {}
LOADED_SOUNDS = {}
LOADED_PROJECTILES = {}

def get_sprite(path, size=(70, 70)):
    '''Loads and returns a sprite from the given path, scaled to the specified size.'''
    key = (path, size)
    if key not in LOADED_SPRITES:
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        LOADED_SPRITES[key] = image
    return LOADED_SPRITES[key]

def get_sound(path, volume=1.0):
    ''' Loads and returns a sound from the given path, setting its volume.'''
    if path not in LOADED_SOUNDS:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        LOADED_SOUNDS[path] = sound
    return LOADED_SOUNDS[path]

def get_projectile_image(path, size=(40, 40)):
    ''' Loads and returns a projectile image from the given path, scaled to the specified size.'''
    key = (path, size)
    if key not in LOADED_PROJECTILES:
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        LOADED_PROJECTILES[key] = image
    return LOADED_PROJECTILES[key]