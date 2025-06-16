# The Last Onion

Object-Oriented Programming 2 university course final project.
A simple rouge-lite game inspired by Brotato, written in Python using Pygame.

## Description

Survive as long as you can in an arena filled with waves of enemies. Collect gold and experience, level up, upgrade your stats, and buy new weapons and items between rounds. 

The game features:

- **Top-down perspective**
- **Multiple weapon types** (sword, scythe, pistol, bow, wand, flame)
- **Level-up and upgrade system**
- **In-game shop between rounds**
- **Various enemy types**
- **Sound effects and music**

## Requirements

- Python 3.8+
- `pygame` library

Install dependencies with:
```bash
pip install pygame
```

## How to Run

From the project root directory, run:
```bash
python main.py
```

## Project Structure

```
.
├── main.py                # Game entry point
├── game.py                # Core game logic and loop
├── player.py              # Player class
├── enemy.py               # Enemy classes
├── weapon.py              # Weapon classes
├── projectile.py          # Projectiles
├── item.py                # Items and passives
├── shop.py                # Shop logic
├── screen.py              # UI, drawing, menus
├── gold.py                # Gold and experience logic
├── profile.py             # Player profile management (optional)
├── settings.py            # Constants and settings
└── src/
    └── sprites/
        ├── backgrounds/
        ├── weapons/
        ├── player.png
        ├── gold_exp.png
        └── ...
```

## Controls

- **W/S/A/D** or **Arrow keys** – Move
- **Space / Enter** – Confirm, attack, select in menu/shop
- **A/D or Arrow keys** – Navigate in menu/upgrades/shop
- **ESC** – Quit

## Authors

- Bartekkk12

## Assets

- Graphics and sounds are either self-made or free to use (CC0).

## License

Open-source project for educational and non-commercial use.