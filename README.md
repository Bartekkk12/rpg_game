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

## Screenshots

All screenshots are located in the `docs/` folder.

### Gameplay
![Gameplay](docs/gameplay.png)

### Shop
![Shop](docs/shop.png)

### Game Over
![Game Over](docs/gameover.png)

## Requirements

- Python 3.8 or higher
- Pygame >= 2.0

---

## Installation

git clone https://github.com/Bartekkk12/rpg_game
cd rpg_game
pip install -r requirements.txt

## How to Run

From the project root directory, run:
```bash
python main.py
```

## Project Structure

```
src/
├── assets/
│   └── assets.py
├── entity/
│   ├── entity.py
│   ├── enemy/
│   │   └── enemy.py
│   └── player/
│       └── player.py
├── game/
│   ├── game.py
│   ├── gold.py
│   ├── item.py
│   ├── screen.py
│   ├── settings.py
│   └── shop.py
├── sprites/
│   ├── backgrounds/
│   ├── weapons/
│   └── ...
├── weapon/
│   ├── projectile.py
│   └── weapon.py
└── main.py
```

## Controls

- **W/S/A/D** or **Arrow keys** – Move
- **Space** – attack
- **Enter** – confirm/select in menus
- **A/D or Arrow keys** – Navigate in menu/upgrades/shop
- **ESC** – Quit

## Tech Stack

- Python
- Pygame
- Object-Oriented Programming (OOP)

## Authors

- Bartekkk12

## Assets

- Graphics and sounds are either self-made or free to use (CC0).

## License

This project is for educational purposes only and is not intended for commercial use.