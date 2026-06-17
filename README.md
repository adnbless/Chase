# Chase

> 2-player game, there's a chaser, there's a player getting chased.

![screenshot]("assets/Images/screenshot.png")

## Description

This project is a local multiplayer tag game built in Python using pygame. Two players share the same keyboard — one tries to escape, the other tries to tag them. The game takes place on a platformer-style map with walls and platforms to navigate. A random teleporter occasionally spawns on the map, which instantly warps whoever touches it to a new random location, adding an unpredictable twist to each round. Whoever is "it" is marked with a downward arrow above their character. The round ends after 60 seconds.

## How to Run

1. Make sure you have **Python 3.13** installed.
2. Install the dependencies:
   *For most of you, this is just `pip install pygame-ce`.*
3. Run the game:
   ```
   python main.py
   ```

## Controls

| Input | Action |
|-------|--------|
| WASD | Move Player 1 (left/right) and jump (W) |
| Arrow Keys | Move Player 2 (left/right) and jump (Up) |
| Esc | Quit |
| Spam jump near a wall | Wall jump |

## Features

- [x] Screen opens to show a title/menu screen before the game starts
- [x] Background image, platform layout, and player images drawn on the screen
- [x] Both players are user-controlled using shared keyboard input
- [x] Tag system — touching the other player flips who is "it", shown by an arrow indicator
- [x] Random teleporter that spawns on the map, warps whoever touches it, and disappears after 5 seconds
- [x] 60-second countdown timer
- [x] Wall jumping
- [x] Background music

## Dependencies

- Python 3.13
- pygame-ce

## Assets

List any images, sounds, fonts, or other files in the `assets/` folder, and where each came from:

- `Images/player.jpg` - 
- `Images/chaser.jpg` - https://www.pinterest.com/pin/minion-wallpaper-hd-yellow-aesthetic--371687775510039267/
- `Images/BACKGROUND.jpeg` - https://www.hobbyconsolas.com/reviews/critica-gru-4-mi-villano-favorito-chute-buen-rollo-veraniego-costa-minions-malvados-entranables-1393499
- `Images/background.jpg` - https://static.wikia.nocookie.net/universalstudios/images/6/60/Otto-minions-the-rise-of-gru-1659537041041.jpeg.webp.jpg/revision/latest?cb=20221104224514
- `Sounds/background.mp3` - https://www.youtube.com/watch?v=Y5hNBTQJVko&list=PLmiWQMMmGPFfhWtgGvU2AaJjYPtrRnt-a&index=2

*(Update any of the above if they came from an outside source and add a link.)*

## Starting Point (Class Code)

- Crown game and Boiler Point


## AI Disclosure

**Model(s) used:** Claude Sonnet 4.6

| Lines / Commit | What it does (in my own words) | Why I used it | AI vs. my own |
|----------------|--------------------------------|---------------|---------------|
| `main.py` lines 9–11 | Sets up the three global teleporter variables — the rect, a timer, and a flag for whether it's currently active | Needed a clean way to track teleporter state across functions | Assisted with AI |
| `main.py` lines 138–147 | `spawn_teleporter()` function — picks a random x/y position on the map and creates a new Rect there, then marks it active and records the spawn time | Needed a reusable function to spawn the teleporter at a random spot | Assisted with AI |
| `main.py` lines 157–165 | Each frame, randomly decides whether to spawn a teleporter (1-in-300 chance) if none is active; also despawns it automatically after 5 seconds | Wanted the teleporter to appear randomly and not last forever | Assisted with AI |
| `main.py` lines 281–292 | Checks each frame if either player's hitbox overlaps the teleporter — if so, teleports that player to a random position and removes the teleporter | Core teleporter gameplay mechanic — warps whoever walks into it | Assisted with AI |
| `main.py` lines 311–320 | Draws the teleporter on screen as a cyan circle if it's currently active | Needed the teleporter to be visible to both players | Assisted with AI |

## Known Bugs / Limitations

- Players can sometimes clip through platforms if moving very fast
- Teleporter can spawn inside a platform, making it hard or impossible to reach

## Possible Future Improvements

- Add a win screen showing who won (whoever wasn't "it" when time ran out)
- Add more special abilities beyond the teleporter (speed boost, freeze, etc.)
- Add sound effects for tagging and teleporting
- Prevent the teleporter from spawning inside platforms

## Author

Aiden C
