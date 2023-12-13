from pathlib import Path
import os

WIDTH = 640
HEIGHT = 480
ZOOM = 2
DATA = Path(os.getcwd()) / "data"

GRID_SIZE = 10
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

CELL_SIZE = 20
