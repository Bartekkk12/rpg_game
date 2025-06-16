import pygame

from settings import *
from item import ITEMS
from math import ceil
from weapon import WEAPONS
from assets import get_sprite

class Screen:
    '''Screen class creating a window.'''
    def __init__(self):
        self._width = WIDTH
        self._height = HEIGHT
        self.surface = pygame.display.set_mode((self._width, self._height))
        self.clock = pygame.time.Clock()

        # Load backgrounds and icon
        self.menu_background = get_sprite("src/sprites/backgrounds/menu_background.png", (self._width, self._height))
        self.game_background = get_sprite("src/sprites/backgrounds/game_background.png", (self._width, self._height))
        self.game_over_background = get_sprite("src/sprites/backgrounds/game_over_background.png", (self._width, self._height))
        self.icon = pygame.image.load("src/sprites/player.png")

        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(self.icon)

    def update(self):
        '''Update the display and tick the clock.'''
        pygame.display.flip()
        self.clock.tick(FPS)
    
    def fill_menu_background(self):
        '''Draw menu background.'''
        self.surface.blit(self.menu_background, (0, 0))

    def fill_game_background(self):
        '''Draw game background.'''
        self.surface.blit(self.game_background, (0, 0))
        
    def display_UI(self, player, enemies, current_round, time_left=None):
        '''Display the in-game UI: round, enemies, HP, level, armor, gold.'''
        self.display_current_round(current_round, time_left)
        self.display_current_enemies_count(enemies)
        self.display_player_current_hp(player)
        self.display_player_current_level(player)
        self.display_player_current_armor(player)
        self.display_player_gold(player)
        
    def menu(self, selected_option):
        '''Display main menu.'''
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
        '''Display HP bar.'''
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
        '''Display Level/XP bar.'''
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
        
    def display_player_current_armor(self, player):
        '''Display armor bar.'''
        bar_width = 200
        bar_height = 25
        bar_x = 10
        bar_y = 80
        
        armor_ratio = player.current_armor / player.max_armor
        armor_bar_width = int(bar_width * armor_ratio)
        
        pygame.draw.rect(self.surface, (0, 0, 0), (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
        pygame.draw.rect(self.surface, (128, 128, 128), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.surface, (80, 80, 80), (bar_x, bar_y, armor_bar_width, bar_height))
        
        font = pygame.font.Font(None, 28)
        text = font.render(f"Armor.{player.current_armor}", True, (255, 255, 255))
        self.surface.blit(text, (80, 83))

    def display_player_gold(self, player):
        '''Display gold amount.'''
        gold_exp = get_sprite("src/sprites/gold_exp.png", (50, 50))
        font = pygame.font.Font(None, 36)
        text = font.render(f"{player.gold}", True, (255, 255, 255))
        self.surface.blit(gold_exp, (5, 110))
        self.surface.blit(text, (55, 128))

    def display_current_round(self, round, time_left=None):
        '''Display current round and timer.'''
        font = pygame.font.Font(None, 36)
        round_text = font.render(f"Round: {round}", True, (255, 255, 255))
        text_width = round_text.get_width()
        x_pos = (WIDTH - text_width) // 2
        self.surface.blit(round_text, (x_pos, 10))
        
        if time_left != None:
            timer_text = font.render(f"{int(time_left)}s", True, (255, 255, 0))
            self.surface.blit(timer_text, (x_pos, 45))

    def display_current_enemies_count(self, enemies):
        '''Display number of enemies left.'''
        font = pygame.font.Font(None, 36)
        round_text = font.render(f"Enemies: {len(enemies)}", True, (255, 255, 255))
        self.surface.blit(round_text, (10, HEIGHT - 40))
        
    def display_game_over_screen(self, wave, selected_option, player):
        '''Display Game Over screen with stats and options.'''
        self.surface.blit(self.game_over_background, (0, 0))

        # display game over text
        title_font = pygame.font.Font(None, 80)
        shadow = title_font.render("Game Over", True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(self._width // 2, 80))
        self.surface.blit(shadow, (shadow_rect.x + 4, shadow_rect.y + 4))
        title = title_font.render("Game Over", True, (255, 80, 80))
        self.surface.blit(title, shadow_rect)

        # Display run won/lost text
        game_over_font = pygame.font.Font(None, 48)
        game_over = game_over_font.render(f"Run Lost on Wave {wave}", True, (255, 255, 255)) if wave < 20 else game_over_font.render("Run Won!", True, (255, 255, 255))
        game_over_rect = game_over.get_rect(center=(self._width // 2, 150))
        self.surface.blit(game_over, game_over_rect)

        # Display stats
        self.display_game_over_stats(player)

        # Display restart/exit buttons
        options = ["Restart", "Exit"]
        options_font = pygame.font.Font(None, 42)
        option_spacing = 60
        button_w, button_h = 200, 60
        total_width = len(options) * button_w + (len(options) - 1) * option_spacing
        start_x = (self._width - total_width) // 2
        options_y = self._height - 130

        for i, txt in enumerate(options):
            x = start_x + i * (button_w + option_spacing)
            rect = pygame.Rect(x, options_y, button_w, button_h)
            color = (255, 220, 80) if selected_option == i+1 else (60, 60, 60)
            pygame.draw.rect(self.surface, color, rect, border_radius=18)
            pygame.draw.rect(self.surface, (255, 255, 255), rect, 3, border_radius=18)

            text_surface = options_font.render(txt, True, (0, 0, 0) if selected_option == i+1 else (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            self.surface.blit(text_surface, text_rect)

    def display_game_over_stats(self, player):
        '''Display player stats at Game Over.'''
        rect_w, rect_h = 400, 340
        rect_x = (self._width - rect_w) // 2
        rect_y = 210
        stats_rect = pygame.Rect(rect_x, rect_y, rect_w, rect_h)

        panel_color = (118, 9, 9)
        border_color = (0, 0, 0)
        pygame.draw.rect(self.surface, panel_color, stats_rect, border_radius=24)
        pygame.draw.rect(self.surface, border_color, stats_rect, 3, border_radius=24)

        # Display title
        font = pygame.font.Font(None, 38)
        stats_title = font.render("Your Stats", True, (255, 255, 255))
        stats_title_rect = stats_title.get_rect(center=(rect_x + rect_w//2, rect_y + 36))
        self.surface.blit(stats_title, stats_title_rect)

        # Display player stats
        stats_font = pygame.font.Font(None, 28)
        stats = [
            ("HP", player.max_hp),
            ("Melee Damage", player.melee_dmg),
            ("Ranged Damage", player.ranged_dmg),
            ("Magic Damage", player.magic_dmg),
            ("Armor", player.max_armor),
            ("Speed", round(player.speed, 2)),
        ]
        start_y = stats_title_rect.bottom + 25
        stat_color = (230, 230, 230)
        for i, (name, val) in enumerate(stats):
            txt = f"{name}: {val}"
            stat_text = stats_font.render(txt, True, stat_color)
            self.surface.blit(stat_text, (rect_x + 40, start_y + i * 40))
        
    def display_level_up_screen(self, upgrade_options, upgrade_selected, upgrade_preview_stats, player):
        '''Display level up selection screen.'''
        self.surface.fill((30, 30, 30))
        font = pygame.font.Font(None, 48)
        title = font.render("Choose an upgrade", True, (255, 255, 255))
        self.surface.blit(title, (self._width // 2 - title.get_width() // 2, 100))

        for i, option in enumerate(upgrade_options):
            color = (255, 255, 0) if i == upgrade_selected else (255, 255, 255)
            upgrade_id = option["id"]
            current_val = upgrade_preview_stats[upgrade_id]

            if upgrade_id in ("Speed"):
                preview_text = f"{upgrade_id}: {current_val:.1f}"
            else:
                preview_text = f"{upgrade_id}: {int(current_val)}"

            text = font.render(preview_text, True, color)
            self.surface.blit(text, (200, 200 + i * 60))
        
        pending_levels = font.render(f"Pending upgrades: {player.pending_level_ups}", True, (255, 255, 255))
        self.surface.blit(pending_levels, (800, 200))
        
    def display_shop_screen(self, shop_selection, items, player, current_round):
        '''Display shop screen with items and weapon upgrades.'''
        # Display shop title and gold
        self.surface.fill((30, 30, 30))
        font = pygame.font.Font(None, 36)
        title = font.render("Shop - Choose an item", True, (255, 255, 255))
        self.surface.blit(title, (self._width // 2 - title.get_width() // 2, 60))
        self.display_player_gold(player)
        
        # Calculate item slots
        item_width = int(self._width * 0.18)
        item_height = int(self._height * 0.45)
        spacing = int(self._width * 0.03)
        total_items_width = 4 * item_width + 3 * spacing
        start_x = (self._width - total_items_width) // 2
        y = self._height // 2 - item_height // 2
        
        # Draw items on screen
        for i, item_key in enumerate(items):
            rect_x = start_x + i * (item_width + spacing)
            rect = pygame.Rect(rect_x, y, item_width, item_height)
            color = (255, 255, 0) if shop_selection == i else (100, 100, 100)
            pygame.draw.rect(self.surface, color, rect, border_radius=12)
            pygame.draw.rect(self.surface, (255, 255, 255), rect, 3, border_radius=12)

            item_font = pygame.font.Font(None, 28)

            # Item bought 
            if item_key is None:
                bought_text = item_font.render("BOUGHT", True, (128, 128, 128))
                self.surface.blit(bought_text, (rect_x + item_width // 2 - bought_text.get_width() // 2, y + item_height // 2 - bought_text.get_height() // 2))
                continue

            if item_key in WEAPONS:
                weapon_key = item_key
                weapon_data = WEAPONS[weapon_key]
                weapon = player.weapons.get(weapon_key)
                img = get_sprite(weapon_data["sprite"], (100, 100))
                img_x = rect_x + (item_width - 100) // 2
                img_y = y + 10
                self.surface.blit(img, (img_x, img_y))
                name_text = item_font.render(weapon_key.replace('_', ' ').title(), True, (0, 0, 0))
                self.surface.blit(name_text, (rect_x + 10, y + 120))
                if weapon is None:
                    price = weapon_data["base_price"]
                    price_text = item_font.render(f"Buy for {price} gold", True, (255, 215, 0))
                    self.surface.blit(price_text, (rect_x + 10, y + 150))
                    effect = f"+{weapon_data['damage']:.2f} dmg, {weapon_data['attack_speed']} atk spd"
                    effect_text = item_font.render(effect, True, (50, 255, 100))
                    self.surface.blit(effect_text, (rect_x + 10, y + 175))
                elif weapon.level < 4:
                    upgrade_price = ceil(weapon_data["base_price"] * (1.6 ** weapon.level))
                    price_lines = [f"Upgrade (lvl {weapon.level})", f"{upgrade_price} gold"]
                    for idx, line in enumerate(price_lines):
                        price_text = item_font.render(line, True, (255, 215, 0))
                        self.surface.blit(price_text, (rect_x + 10, y + 150 + idx * price_text.get_height()))
                    
                    upg_dmg = weapon_data.get("damage/upgrade", 0)
                    upg_spd = weapon_data.get("attack_speed/upgrade", 0)
                    effect_lines = [f"+{upg_dmg} dmg", f"+{upg_spd} atk spd"]
                    for idx, line in enumerate(effect_lines):
                        effect_text = item_font.render(line, True, (50, 255, 100))
                        self.surface.blit(effect_text, (rect_x + 10, y + 195 + idx * effect_text.get_height()))
                else:
                    max_text = item_font.render("Max level!", True, (200, 0, 0))
                    self.surface.blit(max_text, (rect_x + 10, y + 150))
            elif item_key in ITEMS:
                item = ITEMS[item_key]
                if item["image_path"]:
                    img = pygame.transform.scale(pygame.image.load(item["image_path"]), (100, 100))
                    img_x = rect_x + (item_width - 100) // 2
                    img_y = y + 10
                    self.surface.blit(img, (img_x, img_y))
                name_text = item_font.render(item_key.replace('_', ' ').title(), True, (0, 0, 0))
                self.surface.blit(name_text, (rect_x + 10, y + 120))

                price = ceil(item["base_price"] * (current_round * 1.15))
                price_text = item_font.render(f"{price} gold", True, (255, 215, 0))
                self.surface.blit(price_text, (rect_x + 10, y + 150))

                effect = next((f"+{v} {k.replace('_gain_value','').replace('_',' ')}"
                            for k, v in item.items() if k.endswith("_gain_value")), "")
                effect_text = item_font.render(effect, True, (50, 255, 100))
                self.surface.blit(effect_text, (rect_x + 10, y + 175))
        
        # Next round button
        next_round_color = (255, 255, 0) if shop_selection == 4 else (255, 255, 255)
        next_round_text = font.render("Next round (enter)", True, next_round_color)
        rect = next_round_text.get_rect(center=(self._width // 2, self._height - 100))
        self.surface.blit(next_round_text, rect)