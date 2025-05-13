import pygame
from settings import *

class Screen:
    def __init__(self):
        self._width = WIDTH
        self._height = HEIGHT
        self.surface = pygame.display.set_mode((self._width, self._height))
        self.clock = pygame.time.Clock()

        self.menu_background = pygame.transform.scale(pygame.image.load("src/sprites/backgrounds/menu_background.png"), (self._width, self._height))
        self.game_background = pygame.transform.scale(pygame.image.load("src/sprites/backgrounds/game_background.png"), (self._width, self._height))
        self.icon = pygame.image.load("src/sprites/player.png")

        pygame.display.set_caption(TITLE, icontitle="src/sprites/player.png")
        pygame.display.set_icon(self.icon)

    def update(self):
        pygame.display.flip()
        self.clock.tick(FPS)
    
    def fill_menu_background(self):
        self.surface.blit(self.menu_background, (0, 0))

    def fill_game_background(self):
        self.surface.blit(self.game_background, (0, 0))

    def display_player_current_hp(self, player):
        bar_width = 200
        bar_height = 25
        bar_x = 10
        bar_y = 10

        hp_ratio = player.current_hp / player.max_hp
        red_bar_width = int(bar_width * hp_ratio)

        pygame.draw.rect(self.surface, (0, 0, 0), (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
        pygame.draw.rect(self.surface, (128, 128, 128), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.surface, (200, 0, 0), (bar_x, bar_y, red_bar_width, bar_height))

        font = pygame.font.Font(None, 28)
        text = font.render(f"{player.current_hp} / {player.max_hp}", True, (255, 255, 255))
        self.surface.blit(text, (100, 15))

    def display_player_current_level(self, player):
        bar_width = 200
        bar_height = 25
        bar_x = 10
        bar_y = 45

        lvl_ratio = player.exp / player.exp_needed
        lvl_bar_width = int(bar_width * lvl_ratio)

        pygame.draw.rect(self.surface, (0, 0, 0), (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
        pygame.draw.rect(self.surface, (128, 128, 128), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.surface, (0, 217, 0), (bar_x, bar_y, lvl_bar_width, bar_height))

        font = pygame.font.Font(None, 28)
        text = font.render(f"lvl.{player.level}", True, (255, 255, 255))
        self.surface.blit(text, (100, 48))

    def display_player_gold(self, player):
        gold_exp = pygame.transform.scale(pygame.image.load("src/sprites/gold_exp.png"), (50, 50))
        font = pygame.font.Font(None, 36)
        text = font.render(f"{player.gold}", True, (255, 255, 255))
        self.surface.blit(gold_exp, (5, 70))
        self.surface.blit(text, (55, 88))

    def display_current_round(self, round):
        font = pygame.font.Font(None, 36)
        round_text = font.render(f"Round: {round}", True, (255, 255, 255))
        text_width = round_text.get_width()
        x_pos = (WIDTH - text_width) // 2
        self.surface.blit(round_text, (x_pos, 10))

    def display_current_enemies_count(self, enemies):
        font = pygame.font.Font(None, 36)
        round_text = font.render(f"Enemies: {len(enemies)}", True, (255, 255, 255))
        self.surface.blit(round_text, (10, HEIGHT - 40))