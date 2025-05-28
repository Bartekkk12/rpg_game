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
        self.game_over_background = pygame.transform.scale(pygame.image.load("src/sprites/backgrounds/game_over_background.png"), (self._width, self._height))
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
        
    def display_UI(self, player, enemies, current_round):
        self.display_current_round(current_round)
        self.display_current_enemies_count(enemies)
        self.display_player_current_hp(player)
        self.display_player_current_level(player)
        self.display_player_gold(player)
        
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
            option_surface = options_font.render(f"{option_text}", True, color)
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
        
    def display_game_over_screen(self, wave, selected_option, player):
        self.surface.blit(self.game_over_background, (0, 0))
        game_over_font = pygame.font.Font(None, 48)
        game_over = game_over_font.render(f"Run Lost on Wave {wave}", True, (255, 255, 255))
        game_over_rect = game_over.get_rect(center = (self._width // 2, 50))
        self.surface.blit(game_over, game_over_rect)
        self.display_game_over_stats(player)
        
        # display options
        options = ["Restart", "Exit"]
        options_font = pygame.font.Font(None, 42)
        option_spacing = 120

        options_y = 150 + (self._height - 200)

        option_surfaces = [options_font.render(f"{txt}", True, (255,255,0) if i+1==selected_option else (255,255,255)) for i, txt in enumerate(options)]
        total_width = sum(surf.get_width() for surf in option_surfaces) + option_spacing * (len(options) - 1)
        start_x = (self._width - total_width) // 2

        current_x = start_x
        for surf in option_surfaces:
            rect = surf.get_rect(midtop=(current_x + surf.get_width()//2, options_y))
            self.surface.blit(surf, rect)
            current_x += surf.get_width() + option_spacing
        
    def display_game_over_stats(self, player):
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
        
        stats = {
            "HP": player.max_hp,
            "Level": player.level,
            "HP Regen": player.hp_regen,
            "Melee Damage": player.melee_dmg,
            "Ranged Damage": player.ranged_dmg,
            "Magic Damage": player.magic_dmg,
            "Attack Speed": round(player.attack_speed, 2),
            "Range": player.range,
            "Armor": player.armor,
            "Speed": round(player.speed, 2)
        }
        
        start_y = text_rect.bottom + 20
        line_height = 32
        for i, (stat_id, stat) in enumerate(stats.items()):
            stat_text = f"{stat_id}: {stat}"
            rendered = stats_font.render(stat_text, True, (0, 0, 0))
            self.surface.blit(rendered, (stats_rect.left + 20, start_y + i * line_height))
        
        
    def display_level_up_screen(self, upgrade_options, upgrade_selected, upgrade_preview_stats, player):
        self.surface.fill((30, 30, 30))
        font = pygame.font.Font(None, 48)
        title = font.render("Choose an upgrade", True, (255, 255, 255))
        self.surface.blit(title, (self._width // 2 - title.get_width() // 2, 100))

        for i, option in enumerate(upgrade_options):
            color = (255, 255, 0) if i == upgrade_selected else (255, 255, 255)
            upgrade_id = option["id"]
            current_val = upgrade_preview_stats[upgrade_id]

            if upgrade_id in ("Attack Speed", "Speed"):
                preview_text = f"{upgrade_id}: {current_val:.1f}"
            else:
                preview_text = f"{upgrade_id}: {int(current_val)}"

            text = font.render(preview_text, True, color)
            self.surface.blit(text, (200, 200 + i * 60))
        
        pending_levels = font.render(f"Pending upgrades: {player.pending_level_ups}", True, (255, 255, 255))
        self.surface.blit(pending_levels, (800, 200))
        