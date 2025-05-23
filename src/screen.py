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

        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(self.icon)

    def update(self):
        pygame.display.flip()
        self.clock.tick(FPS)
    
    def fill_menu_background(self):
        self.surface.blit(self.menu_background, (0, 0))

    def fill_game_background(self):
        self.surface.blit(self.game_background, (0, 0))
        
    def menu(self, selected_option):
        # settings
        self.fill_menu_background()
        title_font = pygame.font.Font(None, 72)
        options_font = pygame.font.Font(None, 42)

        # display title
        title = title_font.render(TITLE, True, (255, 255, 255))
        title_rect = title.get_rect(center=(self._width // 2, self._height // 2 - 150))
        self.surface.blit(title, title_rect)

        # display options
        options = ["New Game", "Exit"]
        option_spacing = 60
        start_y = self._height // 2 - (len(options) * option_spacing) // 2

        for index, option_text in enumerate(options):
            color = (255, 255, 0) if index + 1 == selected_option else (255, 255, 255)
            option_surface = options_font.render(f"{index + 1}. {option_text}", True, color)
            option_rect = option_surface.get_rect(center=(self._width // 2, start_y + index * option_spacing))
            self.surface.blit(option_surface, option_rect)

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
        
    def display_game_over_screen(self, wave):
        self.surface.fill("grey")
        game_over_font = pygame.font.Font(None, 48)
        game_over = game_over_font.render(f"Run Lost on Wave {wave}", True, (255, 255, 255))
        game_over_rect = game_over.get_rect(center = (self._width // 2, 50))
        self.surface.blit(game_over, game_over_rect)
        self.display_game_over_stats()
        
    def display_game_over_stats(self):
        # overall stats
        rect_width = self._width - 200
        rect_height = self._height - 200
        rect_x = 100
        rect_y = 100
        rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        self.surface.fill("black", rect)
        
        # stats rectangle
        stats_rect_width = rect_width - 800
        stats_rect = pygame.Rect(rect_x, rect_y, stats_rect_width, rect_height)
        self.surface.fill("pink", stats_rect)
        
        # player stats
        font = pygame.font.Font(None, 36)
        stats_font = pygame.font.Font(None, 24)
        text = font.render("Stats", True, (255, 255, 255))
        text_rect = text.get_rect(center=(stats_rect.centerx, rect_y + 25))
        self.surface.blit(text, text_rect)
        
        ### DODAC WYSWIETLANIE STATYSTYK !!! ####
        
        
        
        