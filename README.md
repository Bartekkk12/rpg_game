# The Last Onion

A fast-paced roguelite survival game where you fight endless waves of enemies as a lone onion warrior.

Final project for the Object-Oriented Programming 2 university course.  
Inspired by Brotato. Written in Python with Pygame.

---

## Description

Survive as long as you can in an arena filled with waves of enemies. Collect gold and experience, level up, upgrade your stats, and buy new weapons and items between rounds.

**Features:**
- Top-down perspective
- Multiple weapon types: sword, scythe, pistol, bow, wand, flame
- Level-up and upgrade system
- In-game shop between rounds
- Various unique enemy types
- Sound effects and music

---

## Screenshots

Screenshots are available in the [`docs/`](docs/) folder.

| Gameplay      | Shop          | Game Over    |
| ------------- | ------------- | ------------ |
| ![Gameplay](docs/gameplay.png) | ![Shop](docs/shop.png) | ![Game Over](docs/gameover.png) |

---

## Requirements

- Python 3.8 or higher
- Pygame >= 2.0

---

## Installation

```bash
git clone https://github.com/Bartekkk12/rpg_game
cd rpg_game
pip install -r requirements.txt
```

---

## How to Run

From the project root directory, run:

```bash
python main.py
```

---

## Controls

- **W / A / S / D** or **Arrow keys** – Move
- **Space** – Attack
- **Enter** – Confirm / Select in menus
- **A / D** or **Arrow keys** – Navigate in menus and shop
- **ESC** – Quit the game

---

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

---

## Tech Stack

- Python 3.x
- Pygame
- Object-Oriented Programming (OOP)

---

## Authors

- [Bartekkk12](https://github.com/Bartekkk12)

---

## Assets

Graphics and sounds are either self-made or sourced from free-to-use assets (CC0 license).

---

## License

This project is for educational purposes only and is **not intended for commercial use**.

---