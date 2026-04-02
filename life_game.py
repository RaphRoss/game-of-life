import numpy as np
import time
import os
import argparse

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def initialize_grid(size):
    """Initialise une grille avec des cellules vivantes (1) et mortes (0)."""
    return np.random.choice([0, 1], size=(size, size), p=[0.7, 0.3])  # 70% mortes, 30% vivantes

def count_neighbors(grid, row, col):
    """Compte le nombre de voisins vivants d'une cellule."""
    total = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == 0 and j == 0) or (row + i < 0) or (row + i >= grid.shape[0]) or (col + j < 0) or (col + j >= grid.shape[1]):
                continue
            total += grid[row + i, col + j]
    return total

def update_grid(grid):
    """Met à jour la grille selon les règles du Jeu de la Vie."""
    new_grid = np.copy(grid)
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            neighbors = count_neighbors(grid, row, col)
            if grid[row, col] == 1:  # Cellule vivante
                if neighbors < 2 or neighbors > 3:
                    new_grid[row, col] = 0  # Meurt
            else:  # Cellule morte
                if neighbors == 3:
                    new_grid[row, col] = 1  # Devient vivante
    return new_grid

def print_grid(grid):
    """Affiche la grille."""
    for row in grid:
        print(" ".join(['□' if cell == 1 else '⸱' for cell in row]))

def main(size=20, iterations=100):
    grid = initialize_grid(size)
    
    for _ in range(iterations):
        clear_console()
        print_grid(grid)
        grid = update_grid(grid)
        time.sleep(0.5)  # Pause pour voir les changements


def parse_args():
    parser = argparse.ArgumentParser(description="Jeu de la Vie")
    parser.add_argument(
        "size",
        nargs="?",
        type=int,
        default=20,
        help="taille de la grille (entier > 0)",
    )
    args = parser.parse_args()

    if args.size <= 0:
        parser.error("'size' doit etre un entier strictement positif")

    return args

if __name__ == "__main__":
    arguments = parse_args()
    main(size=arguments.size)
