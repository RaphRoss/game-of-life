import numpy as np
import time
import os
import argparse


PATTERN_LIBRARY = {
    "cellule voyageur": np.array(
        [
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1],
        ],
        dtype=int,
    ),
    "bloc stable": np.array(
        [
            [1, 1],
            [1, 1],
        ],
        dtype=int,
    ),
    "clignotant": np.array(
        [
            [1, 1, 1],
        ],
        dtype=int,
    ),
}


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


def unique_transformations(pattern):
    """Genere les rotations/symetries uniques d'un motif."""
    variants = []
    for k in range(4):
        rotated = np.rot90(pattern, k)
        variants.append(rotated)
        variants.append(np.fliplr(rotated))

    unique = []
    signatures = set()
    for variant in variants:
        signature = tuple(map(tuple, variant.tolist()))
        if signature not in signatures:
            signatures.add(signature)
            unique.append(variant)
    return unique


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
                    window = grid[row:row + height, col:col + width]
                    if np.array_equal(window, pattern):
                        alive_offsets = np.argwhere(pattern == 1)
                        coords = tuple(
                            sorted((row + r, col + c) for r, c in alive_offsets)
                        )
                        detections.append((name, coords))
    return detections


def format_pattern_example(pattern):
    """Transforme un motif en exemple texte simple."""
    lines = []
    for row in pattern:
        lines.append(" ".join("□" if value == 1 else "⸱" for value in row))
    return "\n".join(lines)


def print_summary(stats):
    print("\n===== RESUME DE PARTIE =====")
    print(f"- nb de cellule immortel : {stats['immortal_cells']}")
    print(f"- nb de cellule cree : {stats['created_cells']}")
    print(f"- nb de cellule morte : {stats['dead_cells']}")

    print("\nExemples de types detectes:")
    if not stats["pattern_counts"]:
        print("Aucun motif connu detecte pendant la partie.")
        return

    for name, count in sorted(stats["pattern_counts"].items(), key=lambda item: item[0]):
        print(f"{name} cree : {count}")
        print(format_pattern_example(PATTERN_LIBRARY[name]))
        print()

def print_grid(grid):
    """Affiche la grille."""
    for row in grid:
        print(" ".join(['□' if cell == 1 else '⸱' for cell in row]))

def main(size=20, iterations=100):
    grid = initialize_grid(size)
    immortal_mask = grid == 1

    created_cells = 0
    dead_cells = 0
    seen_pattern_instances = set()
    pattern_counts = {}

    initial_detections = detect_patterns(grid)
    for name, coords in initial_detections:
        signature = (name, coords)
        if signature not in seen_pattern_instances:
            seen_pattern_instances.add(signature)
            pattern_counts[name] = pattern_counts.get(name, 0) + 1
    
    for _ in range(iterations):
        clear_console()
        print_grid(grid)
        new_grid = update_grid(grid)

        # Comptage des transitions cellule morte->vivante et vivante->morte.
        created_cells += int(np.sum((grid == 0) & (new_grid == 1)))
        dead_cells += int(np.sum((grid == 1) & (new_grid == 0)))

        # Une cellule immortelle est vivante au debut et n'est jamais morte.
        immortal_mask &= (new_grid == 1)

        for name, coords in detect_patterns(new_grid):
            signature = (name, coords)
            if signature not in seen_pattern_instances:
                seen_pattern_instances.add(signature)
                pattern_counts[name] = pattern_counts.get(name, 0) + 1

        grid = new_grid
        time.sleep(0.5)  # Pause pour voir les changements

    print_summary(
        {
            "immortal_cells": int(np.sum(immortal_mask)),
            "created_cells": created_cells,
            "dead_cells": dead_cells,
            "pattern_counts": pattern_counts,
        }
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Simulation du Jeu de la Vie (Conway)",
        epilog=(
            "Exemples:\n"
            "  python life_game.py\n"
            "  python life_game.py 30\n"
            "  python life_game.py 30 --cycles 250"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "size",
        nargs="?",
        type=int,
        default=20,
        metavar="TAILLE",
        help="taille de la grille carree (entier > 0)",
    )
    parser.add_argument(
        "-c",
        "--cycles",
        type=int,
        default=100,
        metavar="N",
        help="nombre de cycles de simulation (entier > 0)",
    )
    args = parser.parse_args()

    if args.size <= 0:
        parser.error("'size' doit etre un entier strictement positif")
    if args.cycles <= 0:
        parser.error("'cycles' doit etre un entier strictement positif")

    return args

if __name__ == "__main__":
    arguments = parse_args()
    main(size=arguments.size, iterations=arguments.cycles)
