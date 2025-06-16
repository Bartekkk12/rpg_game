import pygame
import random
import math

from screen import *
from player import *
from enemy import *
from gold import *
from profile import *
from weapon import *
from shop import *
from item import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # screen
        self.screen = Screen()
        self.running = True

        # game
        self.state = "menu"
        self.selected_option = 1
        self.round = 1
        self.round_in_progress = False
        self.round_time = 30  # seconds
        self.round_timer = 0
        self.enemy_spawn_interval = 0.8
        self.enemy_spawn_timer = 0
        self.upgrade_options = []
        self.upgrade_selected = 0
        self.upgrade_preview_stats = {}

        # music
        self.current_ost = None
        self.menu_ost = "src/sprites/music/menu_ost.wav"
        self.game_ost = "src/sprites/music/game_ost.wav"
        
        # player
        self.player = Player()
        
        # enemies
        self.enemies = []
        self.MAX_ENEMIES_ON_SCREEN = 100
        self.max_enemies = 3
        self.dead_enemies_loot = []
        
        # projectiles
        self.projectiles = []
        
        # Shop
        self.shop = Shop()
        self.shop_selection = 0
        self.last_item_selection = 0

    def game(self):
        dt = 1/60
        
        self.screen.fill_game_background()
        keys = pygame.key.get_pressed()
        
        if self.round_in_progress:
            self.round_timer += dt
            self.enemy_spawn_timer += dt

            if (self.enemy_spawn_timer >= self.enemy_spawn_interval and len(self.enemies) < self.MAX_ENEMIES_ON_SCREEN):
                self.enemy_spawn_timer = 0
                self.spawn_enemies(1)

            if self.round_timer > self.round_time:
                self.round_in_progress = False
                self.round += 1
                if self.round > 20:
                    self.state = "victory"
                elif self.player.pending_level_ups > 0:
                    self.generate_upgrade_options()
                    self.state = "level_up"
                else:
                    self.shop.roll_items(self.player)
                    self.shop_selection = 0
                    self.state = "shop"
                return
                    
        for loot in self.dead_enemies_loot[:]:
            if loot.get_rect().colliderect(self.player.get_rect()):
                self.player.gold += loot.amount
                self.player.exp += loot.exp
                self.dead_enemies_loot.remove(loot)
                loot.play_sound()
                if self.player.check_level_up():
                    self.player.level_up()
            else:
                loot.draw(self.screen)
                loot.draw_hit_box(self.screen, (0, 0, 255)) # debugging

        for enemy in self.enemies[:]:
            enemy.follow_player(self.player)
            enemy.draw(self.screen)
            enemy.draw_hit_box(self.screen, (255, 0, 0))  # debugging

            if enemy.current_hp <= 0:
                self.enemies.remove(enemy)
                self.dead_enemies_loot.append(
                    Gold(enemy.x, enemy.y, enemy.enemy_type["gold"], enemy.enemy_type["exp"])
                )
            enemy.attack(self.player)       

        # place weapons
        weapon_list = list(self.player.weapons.values())
        weapon_count = len(weapon_list)
        weapon_sides = []
        if weapon_count == 1:
            weapon_sides = ["center"]
        elif weapon_count == 2:
            weapon_sides = ["left", "right"]
        elif weapon_count == 3:
            weapon_sides = ["left", "right", "left"]
        elif weapon_count == 4:
            weapon_sides = ["left", "right", "left", "right"]
        else:
            weapon_sides = ["left"] * weapon_count

        # projectiles
        for weapon, side in zip(weapon_list, weapon_sides):
            projectile = weapon.attack(self.player, self.enemies, side)
            if projectile:
                self.projectiles.append(projectile)

        for projectile in self.projectiles[:]:
            projectile.update(self.enemies)
            projectile.draw(self.screen)
            for enemy in self.enemies[:]:
                if projectile.get_rect().colliderect(enemy.get_rect()):
                    if projectile.damage >= enemy.current_hp:
                        enemy.current_hp = 0
                        print(f"Projectile hit enemy for {projectile.damage}, Enemy died")
                    else:
                        enemy.current_hp -= projectile.damage
                        print(f"Projectile hit enemy for {projectile.damage}, Enemy health: {enemy.current_hp:.2f}")
                    self.projectiles.remove(projectile)
                    break
            else:
                if projectile.should_remove(self.screen._width, self.screen._height):
                    self.projectiles.remove(projectile) 

        self.player.move(keys)
        self.player.draw(self.screen)
        self.player.draw_weapons(self.screen, self.enemies)
        self.player.regen_hp()  
        self.player.draw_hit_box(self.screen, (0, 255, 0))  # debugging

        if self.player.current_hp <= 0:
            self.state = "game_over"
            
        time_left = max(0, int(self.round_time - self.round_timer)) if self.round_in_progress else None
        self.screen.display_UI(self.player, self.enemies, self.round, time_left)

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
                        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                            if self.selected_option == 1:
                                pygame.mixer.music.stop()
                                self.player.reset_stats()
                                self.round = 1
                                self.start_round()
                                self.state = "game"
                            elif self.selected_option == 2:
                                self.running = False
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
                                    self.player.apply_upgrades(self.upgrade_preview_stats)
                                    self.player.pending_level_ups = 0
                                    self.start_round()
                                    self.shop.roll_items(self.player)
                                    self.shop_selection = 0
                                    self.state = "shop"
                            elif event.key == pygame.K_d and self.player.pending_level_ups > 0:
                                selected = self.upgrade_options[self.upgrade_selected]
                                self.apply_preview_upgrade(selected["id"], 1)
                                self.player.pending_level_ups -= 1
                            elif event.key == pygame.K_a:
                                if self.player.pending_level_ups < self.max_pending_level_ups:
                                    selected = self.upgrade_options[self.upgrade_selected]
                                    self.apply_preview_upgrade(selected["id"], -1)
                                    self.player.pending_level_ups += 1
                    elif self.state == "game_over":
                        if event.key == pygame.K_d:
                            self.selected_option = 2
                        elif event.key == pygame.K_a:
                            self.selected_option = 1
                        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                            if self.selected_option == 1:
                                self.player.reset_stats()
                                self.player.weapons.clear()
                                self.round = 1
                                self.start_round()
                                self.state = "game"
                            elif self.selected_option == 2:
                                self.state = "menu"
                    elif self.state == "victory":
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
                    elif self.state == "shop":
                        if event.key in (pygame.K_a, pygame.K_LEFT):
                            if self.shop_selection in range(1, 4):
                                self.shop_selection -= 1
                        elif event.key in (pygame.K_d, pygame.K_RIGHT):
                            if self.shop_selection in range(0, 3):
                                self.shop_selection += 1
                        elif event.key in (pygame.K_s, pygame.K_DOWN):
                            if self.shop_selection in range(0, 4):
                                self.last_item_selection = self.shop_selection
                                self.shop_selection = 4
                        elif event.key in (pygame.K_w, pygame.K_UP):
                            if self.shop_selection == 4:
                                self.shop_selection = self.last_item_selection
                        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                            if self.shop_selection in range(0, 4):
                                item_key = self.shop.current_items[self.shop_selection]
                                if item_key is None:
                                    print("Przedmiot już kupiony!" if self.shop_selection != 0 else "Brak broni do kupienia na tej pozycji.")
                                    continue

                                if item_key in WEAPONS:
                                    # BROŃ (kup lub ulepsz)
                                    weapon_key = item_key
                                    weapon_data = WEAPONS[weapon_key]
                                    weapon = self.player.weapons.get(weapon_key)
                                    if weapon is None:
                                        price = weapon_data["base_price"]
                                        if self.player.gold >= price:
                                            self.player.gold -= price
                                            # Tworzenie odpowiedniego typu broni:
                                            if weapon_key in ["pistol", "bow"]:
                                                weapon_obj = Ranged_Weapon(weapon_key)
                                            elif weapon_key in ["magic_wand", "pyromancy_flame"]:
                                                weapon_obj = Magic_Weapon(weapon_key)
                                            elif weapon_key in ["sword", "scythe"]:
                                                weapon_obj = Melee_Weapon(weapon_key)
                                            self.player.weapons[weapon_key] = weapon_obj
                                            self.shop.current_items[self.shop_selection] = None
                                            print(f"Kupiono nową broń: {weapon_key}")
                                        else:
                                            print("Za mało złota, by kupić broń.")
                                    elif weapon.level < 4:
                                        upgrade_price = math.ceil(weapon_data["base_price"] * (1.3 ** weapon.level))
                                        if self.player.gold >= upgrade_price:
                                            self.player.gold -= upgrade_price
                                            weapon.apply_upgrades()
                                            self.shop.current_items[self.shop_selection] = None
                                            print(f"Ulepszono {weapon_key} do poziomu {weapon.level}")
                                        else:
                                            print("Za mało złota, by ulepszyć broń.")
                                    else:
                                        print("Broń ma już maksymalny poziom!")
                                elif item_key in ITEMS:
                                    # ITEM (dowolny slot)
                                    item_info = ITEMS[item_key]
                                    price = math.ceil(item_info["base_price"] * (self.round * 1.15))
                                    if self.player.gold >= price:
                                        self.player.gold -= price
                                        item = Item(item_key)
                                        item.apply_upgrades(self.player)
                                        self.shop.current_items[self.shop_selection] = None
                                        print(f"Kupiono przedmiot {item_key}")
                                    else:
                                        print("Za mało złota")
                                else:
                                    print("Nieznany przedmiot/klucz w sklepie!")
                            elif self.shop_selection == 4:
                                self.shop.roll_items(self.player)
                                self.start_round()
                                self.state = "game"
                        
            # game states
            if self.state == "menu":
                if not pygame.mixer.music.get_busy() or self.current_ost != "menu":
                    pygame.mixer.music.load(self.menu_ost)
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0) # debugging
                    self.current_ost = "menu"
                self.screen.menu(self.selected_option)
            elif self.state == "game":
                if not pygame.mixer.music.get_busy() or self.current_ost != "game":
                    pygame.mixer.music.load(self.game_ost)
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0) # debugging
                    self.current_ost = "game"
                self.game()
            elif self.state == "level_up":
                pygame.mixer.music.stop()
                self.screen.display_level_up_screen(self.upgrade_options, self.upgrade_selected, self.upgrade_preview_stats, self.player)
            elif self.state == "shop":
                self.screen.display_shop_screen(self.shop_selection, self.shop.current_items, self.player, self.round)
            elif self.state == "game_over":
                pygame.mixer.music.stop()
                self.screen.display_game_over_screen(self.round, self.selected_option, self.player)
            elif self.state == "victory":
                pygame.mixer.music.stop()
                self.screen.display_game_over_screen(self.round, self.selected_option, self.player)
                
            self.screen.update()

        pygame.quit()

    def start_round(self):
        self.set_enemy_spawn_interval()
        if "pistol" not in self.player.weapons:
            self.player.weapons["pistol"] = Ranged_Weapon("pistol")
        self.dead_enemies_loot.clear()
        self.projectiles.clear()
        self.player.current_hp = self.player.max_hp
        self.player.current_armor = self.player.max_armor
        self.enemies = []
        self.round_in_progress = True
        self.round_timer = 0
        self.enemy_spawn_timer = 0

    def spawn_enemies(self, count):
        spawned = 0
        tries_limit = 100
        max_enemies_on_screen = min(self.MAX_ENEMIES_ON_SCREEN, self.max_enemies + self.round * 2)
        available_enemies = [name for name, data in ENEMIES.items() if data["spawn_wave"] <= self.round]
        while spawned < count and len(self.enemies) < max_enemies_on_screen:
            tries = 0
            while tries < tries_limit:
                x = random.randint(0, self.screen._width - 50)
                y = random.randint(0, self.screen._height - 50)
                dx = x - self.player.x
                dy = y - self.player.y
                distance = math.hypot(dx, dy)
                if distance >= 150:
                    break
                tries += 1
            if available_enemies:
                self.enemies.append(Enemy(random.choice(available_enemies), x, y, self.round))
                spawned += 1

    def generate_upgrade_options(self):
        self.max_pending_level_ups = self.player.pending_level_ups
        self.upgrade_options = [
            {"id": "HP"},
            {"id": "Melee Damage"},
            {"id": "Ranged Damage"},
            {"id": "Magic Damage"},
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
            "Range": self.player.range,
            "Armor": self.player.max_armor,
            "Speed": self.player.speed
        }

    def apply_preview_upgrade(self, upgrade_id, direction):
        base_stats = {
            "HP": self.player.max_hp,
            "Melee Damage": self.player.melee_dmg,
            "Ranged Damage": self.player.ranged_dmg,
            "Magic Damage": self.player.magic_dmg,
            "Range": self.player.range,
            "Armor": self.player.max_armor,
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
        elif upgrade_id == "Range":
            self.upgrade_preview_stats["Range"] += direction
        elif upgrade_id == "Armor":
            self.upgrade_preview_stats["Armor"] += direction
        elif upgrade_id == "Speed":
            self.upgrade_preview_stats["Speed"] += 0.4 * direction
            
    def set_enemy_spawn_interval(self):
        if self.round < 5:
            self.enemy_spawn_interval = 0.8 
        elif 5 <= self.round < 10:
            self.enemy_spawn_interval = 0.6
        elif 10 <= self.round < 15:
            self.enemy_spawn_interval = 0.4
        else:
            self.enemy_spawn_interval = 0.3
