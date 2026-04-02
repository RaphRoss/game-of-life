import time
import os
import numpy as np

from cli import parse_args
from display import print_grid, print_summary
from simulation import detect_patterns, initialize_grid, update_grid


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

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

if __name__ == "__main__":
    arguments = parse_args()
    main(size=arguments.size, iterations=arguments.cycles)
