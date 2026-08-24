# Space Shooter 🚀

<img width="1311" height="843" alt="Στιγμιότυπο οθόνης 2026-05-25 180441" src="https://github.com/user-attachments/assets/15809e5d-69da-480e-ac54-d2c8efadef54" />

A classic, endless 2D side-scrolling space shooter built with Python and Pygame. Survive as long as you can by dodging enemy ships and meteors, and grab power-ups to keep your ship flying.

## Features
* **Fluid Movement:** Full 8-way directional movement using WASD.
* **Dynamic Hazards:** Randomized enemy ship and meteor spawning to keep you on your toes.
* **Power-Up System:**
  * 🛡️ **Shields:** Grants 10 seconds of invulnerability (custom sprite overlay included).
  * 💚 **Heals:** Restores lost lives (capped at 10).
* **Score & High Score Tracking:** Your survival time is your score, and your best run is saved to `highscore.txt` so it persists between sessions.
* **Responsive Scaling:** Built-in dynamic scaling for entity graphics so they match your screen resolution naturally.

## Controls
| Key | Action |
| --- | --- |
| `W` / `A` / `S` / `D` | Move your ship up / left / down / right |
| `Esc` | Quit the game |

You have 10 lives — colliding with an enemy ship or meteor costs you a life (unless your shield is active). Survive as long as possible to rack up score; the game ends when you run out of lives.

## Installation

### Prerequisites
Make sure you have [Python 3.x](https://www.python.org/downloads/) and [Pygame](https://www.pygame.org) installed on your machine.

```bash
pip install pygame
```

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/mariospropapadimas-dev/SpaceShooterGame-Python.git
   cd SpaceShooterGame-Python
   ```
2. Run the game:
   ```bash
   python main.py
   ```

## Project Structure
```
SpaceShooterGame-Python/
├── main.py         # Game loop, event handling, collisions, and HUD
├── player.py        # Player ship movement and rendering
├── enemy.py         # Enemy ship behavior
├── meteor.py         # Meteor hazard behavior
├── shield.py         # Shield power-up
├── heal.py         # Heal power-up
├── gamestate.py       # Score tracking and high score persistence
├── resources.py        # Shared image loading and screen configuration
├── assets/          # Sprites and background images
└── highscore.txt       # Persisted high score
```
