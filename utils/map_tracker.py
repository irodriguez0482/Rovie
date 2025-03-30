# utils/map_tracker.py

import csv
from pathlib import Path

# Grid is 3 rows by 3 columns (each line = 1 meter wide assuming equal spacing)
GRID_SIZE = 3

# Map states
UNKNOWN = "UNKNOWN"
CLEAR = "CLEAR"
OBSTACLE = "OBSTACLE"

# Initialize 3x3 grid
map_grid = [[UNKNOWN for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def mark_cell(row, col, status):
    """Mark a cell in the grid with CLEAR or OBSTACLE."""
    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        map_grid[row][col] = status

def save_map_to_csv(filepath="logs/map_grid.csv"):
    Path("logs").mkdir(exist_ok=True)
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Row", "Col", "Status"])
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                writer.writerow([row, col, map_grid[row][col]])

def print_map():
    print("\n=== ROVER MAP STATUS ===")
    for row in map_grid:
        print(" | ".join(row))
    print("========================\n")
