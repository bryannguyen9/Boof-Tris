# BOOF-TRIS

A small “Tetris-style” falling-blocks game built with Pygame, featuring:

- **Home Menu** with “Start Game” and “Leaderboard”  
- **In-game** scoring and two background tracks  
- **Game Over** screen with “Play Again,” “Main Menu,” and “Save Score”  
- **Persistent leaderboard** stored in a DuckDB file

## 🎯 Features
### Live Scoring

3-block match → 10 points

4-block match → 25 points

5+ block match → 50 points

### Leaderboard Persistence

On “Save Score,” enter a name (1–10 alphanumeric chars).

Scores are stored in a local DuckDB file (leaderboard.duckdb).

Top 10 only; old low scores are trimmed automatically.

Each entry also records the date you achieved it.

## 🚀 Controls
← / → : move block left/right

Space : rotate block


## 🔧 Prerequisites

- **Python 3.8+**  
- **pip** (Python package manager)

---

## 🛠️ Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/<your-username>/boof-tris.git
   cd boof-tris

2. Install dependencies
    ```bash
    pip install -r requirements.txt

3. Run the game!
    ```bash
    python src/main.py



