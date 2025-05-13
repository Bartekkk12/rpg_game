import pygame
import random
from screen import *
from player import *
from enemy import *
from settings import TITLE

class Game:
    def __init__(self):
        pygame.init()

        self.screen = Screen()
        self.running = True

        self.state = "menu"
        self.selected_option = 1
        self.round = 1
        self.round_in_progress = False
        self.upgrade_options = []
        self.upgrade_selected = 0
        self.upgrade_preview_stats = {}

        self.player = Player("player")

        self.enemies = []
        self.max_enemies = 3
        self.dead_enemies_loot = []

        self.gold = pygame.transform.scale(pygame.image.load("src/sprites/gold_exp.png"), (50, 50))

    def menu(self):
        self.screen.fill_menu_background()
        title_font = pygame.font.Font(None, 72)
        options_font = pygame.font.Font(None, 42)

        title = title_font.render(TITLE, True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen._width // 2, self.screen._height // 2 - 150))
        self.screen.surface.blit(title, title_rect)

        options = ["New Game", "Exit"]
        option_spacing = 60
        start_y = self.screen._height // 2 - (len(options) * option_spacing) // 2

        for index, option_text in enumerate(options):
            color = (255, 255, 0) if index + 1 == self.selected_option else (255, 255, 255)
            option_surface = options_font.render(f"{index + 1}. {option_text}", True, color)
            option_rect = option_surface.get_rect(center=(self.screen._width // 2, start_y + index * option_spacing))
            self.screen.surface.blit(option_surface, option_rect)

    def game(self):
        self.screen.fill_game_background()
        keys = pygame.key.get_pressed()

        for loot in self.dead_enemies_loot[:]:
            loot_rect = pygame.Rect(loot["x"], loot["y"], 10, 10)
            player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)

            if loot_rect.colliderect(player_rect):
                self.player.gold += loot["gold"]
                self.player.exp += loot["exp"]
                self.dead_enemies_loot.remove(loot)

                if self.player.check_level_up():
                    self.player.level_up()
            else:
                self.screen.surface.blit(self.gold, (loot["x"], loot["y"]))

        for enemy in self.enemies[:]:
            enemy.follow_player(self.player)
            enemy.draw(self.screen)

            if enemy.current_hp <= 0:
                self.enemies.remove(enemy)
                self.dead_enemies_loot.append({
                    "x": enemy.x,
                    "y": enemy.y,
                    "gold": enemy.enemy_type["gold"],
                    "exp": enemy.enemy_type["exp"]
                })

            enemy.attack(self.player)

        self.player.move(keys)
        self.player.draw(self.screen)
        self.player.attack(self.enemies)

        if self.round_in_progress and not self.enemies:
            self.round_in_progress = False
            self.round += 1
            if self.round > 20:
                self.state = "victory"
            elif self.player.pending_level_ups > 0:
                self.generate_upgrade_options()
                self.state = "upgrade"
            else:
                self.start_round()

        self.screen.display_current_round(self.round)
        self.screen.display_current_enemies_count(self.enemies)
        self.screen.display_player_current_hp(self.player)
        self.screen.display_player_current_level(self.player)
        self.screen.display_player_gold(self.player)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.state == "menu":
                        if event.key in (pygame.K_w, pygame.K_UP):
                            self.selected_option = 1
                        elif event.key in (pygame.K_s, pygame.K_DOWN):
                            self.selected_option = 2
                        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            if self.selected_option == 1:
                                self.round = 1
                                self.start_round()
                                self.state = "game"
                            elif self.selected_option == 2:
                                self.running = False
                    elif self.state == "upgrade":
                        if self.upgrade_options:
                            if event.key in (pygame.K_w, pygame.K_UP):
                                self.upgrade_selected = (self.upgrade_selected - 1) % len(self.upgrade_options)
                            elif event.key in (pygame.K_s, pygame.K_DOWN):
                                self.upgrade_selected = (self.upgrade_selected + 1) % len(self.upgrade_options)
                            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                                selected = self.upgrade_options[self.upgrade_selected]
                                self.apply_upgrade(selected["id"])
                                self.player.pending_level_ups -= 1
                                if self.player.pending_level_ups > 0:
                                    self.generate_upgrade_options()
                                else:
                                    self.start_round()
                                    self.state = "game"
                            elif event.key == pygame.K_d and self.player.pending_level_ups > 0:
                                selected = self.upgrade_options[self.upgrade_selected]
                                self.apply_preview_upgrade(selected["id"], 1)
                                self.player.pending_level_ups -= 1
                            elif event.key == pygame.K_a:
                                selected = self.upgrade_options[self.upgrade_selected]
                                self.apply_preview_upgrade(selected["id"], -1)
                                self.player.pending_level_ups += 1

            if self.state == "menu":
                self.menu()
            elif self.state == "game":
                self.game()
            elif self.state == "upgrade":
                self.upgrade()

            self.screen.update()

        pygame.quit()

    def start_round(self):
        self.dead_enemies_loot.clear()
        self.player.current_hp = self.player.max_hp
        self.enemies = []
        self.round_in_progress = True
        enemy_count = self.max_enemies + self.round * 2

        for _ in range(enemy_count):
            x = random.randint(0, self.screen._width - 50)
            y = random.randint(0, self.screen._height - 50)
            self.enemies.append(Enemy("zombie_cabbage", x, y))

    def upgrade(self):
        self.screen.surface.fill((30, 30, 30))
        font = pygame.font.Font(None, 48)
        title = font.render("Choose an upgrade", True, (255, 255, 255))
        self.screen.surface.blit(title, (self.screen._width // 2 - title.get_width() // 2, 100))

        for i, option in enumerate(self.upgrade_options):
            color = (255, 255, 0) if i == self.upgrade_selected else (255, 255, 255)
            upgrade_id = option["id"]
            
            current_val = self.upgrade_preview_stats[upgrade_id]
            if upgrade_id == "Attack Speed":
                preview_text = f"{upgrade_id}: {current_val:.1f}"
            else:
                preview_text = f"{upgrade_id}: {int(current_val)}"
            
            text = font.render(f"{option['desc']} | {preview_text}", True, color)
            self.screen.surface.blit(text, (200, 200 + i * 60))

    def generate_upgrade_options(self):
        p = self.player
        self.upgrade_options = [
            {"id": "HP", "desc": f"HP ({p.max_hp} → {p.max_hp + 1})"},
            {"id": "Melee Damage", "desc": f"Melee Damage ({p.melee_dmg} → {p.melee_dmg + 1})"},
            {"id": "Ranged Damage", "desc": f"Ranged Damage ({p.ranged_dmg} → {p.ranged_dmg + 1})"},
            {"id": "Magic Damage", "desc": f"Magic Damage ({p.magic_dmg} → {p.magic_dmg + 1})"},
            {"id": "Attack Speed", "desc": f"Attack Speed ({p.attack_speed:.1f} → {p.attack_speed + 0.1:.1f})"},
            {"id": "Range", "desc": f"Range ({p.range} → {p.range + 10})"},
            {"id": "Armor", "desc": f"Armor ({p.armor} → {p.armor + 1})"},
            {"id": "Speed", "desc": f"Speed ({p.speed} → {p.speed + 1})"},
        ]
        self.upgrade_selected = 0
        self.upgrade_preview_stats = {
            "HP": self.player.max_hp,
            "Melee Damage": self.player.melee_dmg,
            "Ranged Damage": self.player.ranged_dmg,
            "Magic Damage": self.player.magic_dmg,
            "Attack Speed": self.player.attack_speed,
            "Range": self.player.range,
            "Armor": self.player.armor,
            "Speed": self.player.speed
        }

    def apply_upgrade(self, upgrade_id):
        p = self.player
        if upgrade_id == "HP":
            p.max_hp += 1
            p.current_hp = p.max_hp
        elif upgrade_id == "Melee Damage":
            p.melee_dmg += 1
        elif upgrade_id == "Ranged Damage":
            p.ranged_dmg += 1
        elif upgrade_id == "Magic Damage":
            p.magic_dmg += 1
        elif upgrade_id == "Attack Speed":
            p.attack_speed += 0.1
        elif upgrade_id == "Range":
            p.range += 10
        elif upgrade_id == "Armor":
            p.armor += 1
        elif upgrade_id == "Speed":
            p.speed += 1

    def apply_preview_upgrade(self, upgrade_id, direction):
        if upgrade_id == "HP":
            self.upgrade_preview_stats["HP"] += direction
        elif upgrade_id == "Melee Damage":
            self.upgrade_preview_stats["Melee Damage"] += direction
        elif upgrade_id == "Ranged Damage":
            self.upgrade_preview_stats["Ranged Damage"] += direction
        elif upgrade_id == "Magic Damage":
            self.upgrade_preview_stats["Magic Damage"] += direction
        elif upgrade_id == "Attack Speed":
            self.upgrade_preview_stats["Attack Speed"] += 0.1 * direction
        elif upgrade_id == "Range":
            self.upgrade_preview_stats["Range"] += 10 * direction
        elif upgrade_id == "Armor":
            self.upgrade_preview_stats["Armor"] += direction
        elif upgrade_id == "Speed":
            self.upgrade_preview_stats["Speed"] += direction

