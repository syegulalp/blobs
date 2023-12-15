from pathlib import Path
import os

WIDTH = 640
HEIGHT = 480
ZOOM = 2
GRID_SIZE = 10
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Size for each cell in the collision detection grid.
# The ideal size is slightly larger than the largest
# game element you want to detect collisions for.

CELL_SIZE = 20

DATA = Path(os.getcwd()) / "data"
