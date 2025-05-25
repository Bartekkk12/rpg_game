import pygame
import random

from screen import *
from player import *
from enemy import *
from settings import TITLE

class Game:
    def __init__(self):
        pygame.init()

        # screen
        self.screen = Screen()
        self.running = True

        # game
        self.state = "menu"
        self.selected_option = 1
        self.round = 1
        self.round_in_progress = False
        self.upgrade_options = []
        self.upgrade_selected = 0
        self.upgrade_preview_stats = {}

        # player
        self.player = Player("player")

        # enemies
        self.enemies = []
        self.max_enemies = 3
        self.dead_enemies_loot = []
        self.gold = pygame.transform.scale(pygame.image.load("src/sprites/gold_exp.png"), (50, 50))

    def game(self):
        self.screen.fill_game_background()
        keys = pygame.key.get_pressed()

        # draw loot after killing enemy
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

        # drawe enemies
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

        # player movement
        self.player.move(keys)
        self.player.draw(self.screen)
        self.player.attack(self.enemies)

        # round state
        if self.player.current_hp > 0:
            if self.round_in_progress and not self.enemies:
                self.round_in_progress = False
                self.round += 1
                if self.round > 20:
                    self.state = "victory"
                elif self.player.pending_level_ups > 0:
                    self.generate_upgrade_options()
                    self.state = "level_up"
                else:
                    self.start_round()
        else:
            self.state = "game_over"
            
        # UI
        self.screen.display_UI(self.player, self.enemies, self.round)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    # main menu
                    if self.state == "menu":
                        if event.key in (pygame.K_w, pygame.K_UP):
                            self.selected_option = 1
                        elif event.key in (pygame.K_s, pygame.K_DOWN):
                            self.selected_option = 2
                        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                            if self.selected_option == 1:
                                self.round = 1
                                self.start_round()
                                self.state = "game"
                            elif self.selected_option == 2:
                                self.running = False
                    # upgrade 
                    elif self.state == "level_up":
                        if self.upgrade_options:
                            if event.key in (pygame.K_w, pygame.K_UP):
                                self.upgrade_selected = (self.upgrade_selected - 1) % len(self.upgrade_options)
                            elif event.key in (pygame.K_s, pygame.K_DOWN):
                                self.upgrade_selected = (self.upgrade_selected + 1) % len(self.upgrade_options)
                            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                                if self.player.pending_level_ups > 1:
                                    self.player.pending_level_ups -= 1
                                else:
                                    self.set_upgrades()
                                    self.player.pending_level_ups = 0
                                    self.start_round()
                                    self.state = "game"
                            elif event.key == pygame.K_d and self.player.pending_level_ups > 0:
                                selected = self.upgrade_options[self.upgrade_selected]
                                self.apply_preview_upgrade(selected["id"], 1)
                                self.player.pending_level_ups -= 1
                            elif event.key == pygame.K_a:
                                if self.player.pending_level_ups < self.max_pending_level_ups:
                                    selected = self.upgrade_options[self.upgrade_selected]
                                    self.apply_preview_upgrade(selected["id"], -1)
                                    self.player.pending_level_ups += 1
                    # game over                
                    elif self.state == "game_over":
                        if event.key == pygame.K_d:
                            self.selected_option = 2
                        elif event.key == pygame.K_a:
                            self.selected_option = 1
                        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                            if self.selected_option == 1:
                                self.player.reset_stats()
                                self.round = 1
                                self.start_round()
                                self.state = "game"
                            elif self.selected_option == 2:
                                self.state = "menu"
            # game states
            if self.state == "menu":
                self.screen.menu(self.selected_option)
            elif self.state == "game":
                self.game()
            elif self.state == "level_up":
                self.level_up()
            elif self.state == "game_over":
                self.screen.display_game_over_screen(self.round, self.selected_option)
                
            self.screen.update()

        pygame.quit()

    def start_round(self):
        # round start
        self.dead_enemies_loot.clear()
        self.player.current_hp = self.player.max_hp
        self.enemies = []
        self.round_in_progress = True
        enemy_count = self.max_enemies + self.round * 2

        # draw enemies in random position
        for _ in range(enemy_count):
            x = random.randint(0, self.screen._width - 50)
            y = random.randint(0, self.screen._height - 50)
            ### draw random enemies!!!! ###
            self.enemies.append(Enemy("zombie_cabbage", x, y))
            ### draw random enemies!!!! ###

    def level_up(self):
        self.screen.surface.fill((30, 30, 30))
        font = pygame.font.Font(None, 48)
        title = font.render("Choose an upgrade", True, (255, 255, 255))
        self.screen.surface.blit(title, (self.screen._width // 2 - title.get_width() // 2, 100))

        for i, option in enumerate(self.upgrade_options):
            color = (255, 255, 0) if i == self.upgrade_selected else (255, 255, 255)
            
            upgrade_id = option["id"]
            current_val = self.upgrade_preview_stats[upgrade_id]
            
            preview_text = f"{upgrade_id}: {current_val:.1f}" if upgrade_id == "Attack Speed" else f"{upgrade_id}: {int(current_val)}"
            
            text = font.render(f"{preview_text}", True, color)
            self.screen.surface.blit(text, (200, 200 + i * 60))
            
        pending_levels = font.render(f"Pending upgrades: {self.player.pending_level_ups}", True, (255, 255, 255))
        self.screen.surface.blit(pending_levels, (800, 200))

    def generate_upgrade_options(self):
        self.max_pending_level_ups = self.player.pending_level_ups
        self.upgrade_options = [
            {"id": "HP"},
            {"id": "Melee Damage"},
            {"id": "Ranged Damage"},
            {"id": "Magic Damage"},
            {"id": "Attack Speed"},
            {"id": "Range"},
            {"id": "Armor"},
            {"id": "Speed"},
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
        if upgrade_id == "HP":
            self.player.max_hp += 1
        elif upgrade_id == "Melee Damage":
            self.player.melee_dmg += 1
        elif upgrade_id == "Ranged Damage":
            self.player.ranged_dmg += 1
        elif upgrade_id == "Magic Damage":
            self.player.magic_dmg += 1
        elif upgrade_id == "Attack Speed":
            self.player.attack_speed += 0.1
        elif upgrade_id == "Range":
            self.player.range += 10
        elif upgrade_id == "Armor":
            self.player.armor += 1
        elif upgrade_id == "Speed":
            self.player.speed += 1

    def apply_preview_upgrade(self, upgrade_id, direction):
        base_stats = {
            "HP": self.player.max_hp,
            "Melee Damage": self.player.melee_dmg,
            "Ranged Damage": self.player.ranged_dmg,
            "Magic Damage": self.player.magic_dmg,
            "Attack Speed": self.player.attack_speed,
            "Range": self.player.range,
            "Armor": self.player.armor,
            "Speed": self.player.speed
        }
        if direction == -1:
            if self.upgrade_preview_stats[upgrade_id] <= base_stats[upgrade_id]:
                return
        
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

    def set_upgrades(self):
        self.player.max_hp = self.upgrade_preview_stats["HP"]
        self.player.melee_dmg = self.upgrade_preview_stats["Melee Damage"]
        self.player.ranged_dmg = self.upgrade_preview_stats["Ranged Damage"]
        self.player.magic_dmg = self.upgrade_preview_stats["Magic Damage"]
        self.player.attack_speed = self.upgrade_preview_stats["Attack Speed"]
        self.player.range = self.upgrade_preview_stats["Range"]
        self.player.armor = self.upgrade_preview_stats["Armor"]
        self.player.speed = self.upgrade_preview_stats["Speed"]