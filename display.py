from patterns import PATTERN_LIBRARY


def format_pattern_example_lines(pattern):
    """Transforme un motif en lignes texte simples."""
    lines = []
    for row in pattern:
        lines.append(" ".join("□" if value == 1 else "⸱" for value in row))
    return lines


def print_pattern_pair(left_entry, right_entry=None, column_width=50):
    """Affiche deux motifs cote a cote avec stats sur une seule ligne."""
    left_name, left_count = left_entry
    left_header = f"{left_name} cree : {left_count}"

    if right_entry is None:
        print(left_header)
        for line in format_pattern_example_lines(PATTERN_LIBRARY[left_name]):
            print(line)
        print()
        return

    right_name, right_count = right_entry
    right_header = f"{right_name} cree : {right_count}"
    print(f"{left_header.ljust(column_width)}{right_header}")

    left_lines = format_pattern_example_lines(PATTERN_LIBRARY[left_name])
    right_lines = format_pattern_example_lines(PATTERN_LIBRARY[right_name])
    max_lines = max(len(left_lines), len(right_lines))

    for idx in range(max_lines):
        left_line = left_lines[idx] if idx < len(left_lines) else ""
        right_line = right_lines[idx] if idx < len(right_lines) else ""
        print(f"{left_line.ljust(column_width)}{right_line}")
    print()


def print_summary(stats):
    print("\n===== RESUME DE PARTIE =====")
    print(f"- nb de cellule immortel : {stats['immortal_cells']}")
    print(f"- nb de cellule cree : {stats['created_cells']}")
    print(f"- nb de cellule morte : {stats['dead_cells']}")

    print("\nExemples de types detectes:")
    if not stats["pattern_counts"]:
        print("Aucun motif connu detecte pendant la partie.")
        return

    entries = sorted(stats["pattern_counts"].items(), key=lambda item: item[0])
    for idx in range(0, len(entries), 2):
        left_entry = entries[idx]
        right_entry = entries[idx + 1] if idx + 1 < len(entries) else None
        print_pattern_pair(left_entry, right_entry)


def print_grid(grid):
    """Affiche la grille."""
    for row in grid:
        print(" ".join(["□" if cell == 1 else "⸱" for cell in row]))
