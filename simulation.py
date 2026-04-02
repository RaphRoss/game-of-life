import numpy as np

from patterns import PATTERN_LIBRARY, unique_transformations


def initialize_grid(size):
    """Initialise une grille avec des cellules vivantes (1) et mortes (0)."""
    return np.random.choice([0, 1], size=(size, size), p=[0.7, 0.3])


def count_neighbors(grid, row, col):
    """Compte le nombre de voisins vivants d'une cellule."""
    total = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (
                (i == 0 and j == 0)
                or (row + i < 0)
                or (row + i >= grid.shape[0])
                or (col + j < 0)
                or (col + j >= grid.shape[1])
            ):
                continue
            total += grid[row + i, col + j]
    return total


def update_grid(grid):
    """Met a jour la grille selon les regles du Jeu de la Vie."""
    new_grid = np.copy(grid)
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            neighbors = count_neighbors(grid, row, col)
            if grid[row, col] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[row, col] = 0
            else:
                if neighbors == 3:
                    new_grid[row, col] = 1
    return new_grid


def detect_patterns(grid):
    """Detecte des motifs connus dans la grille et renvoie leurs positions."""
    detections = []

    for name, base_pattern in PATTERN_LIBRARY.items():
        for pattern in unique_transformations(base_pattern):
            height, width = pattern.shape
            if grid.shape[0] < height or grid.shape[1] < width:
                continue

            for row in range(grid.shape[0] - height + 1):
                for col in range(grid.shape[1] - width + 1):
                    window = grid[row : row + height, col : col + width]
                    if np.array_equal(window, pattern):
                        alive_offsets = np.argwhere(pattern == 1)
                        coords = tuple(sorted((row + r, col + c) for r, c in alive_offsets))
                        detections.append((name, coords))
    return detections
