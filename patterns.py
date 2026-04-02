import numpy as np


PATTERN_LIBRARY = {
    "bloc stable": np.array(
        [
            [1, 1],
            [1, 1],
        ],
        dtype=int,
    ),
    "ruche": np.array(
        [
            [0, 1, 1, 0],
            [1, 0, 0, 1],
            [0, 1, 1, 0],
        ],
        dtype=int,
    ),
    "pain": np.array(
        [
            [0, 1, 1, 0],
            [1, 0, 0, 1],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
        ],
        dtype=int,
    ),
    "bateau": np.array(
        [
            [1, 1, 0],
            [1, 0, 1],
            [0, 1, 0],
        ],
        dtype=int,
    ),
    "bassine": np.array(
        [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0],
        ],
        dtype=int,
    ),
    "cellule voyageur": np.array(
        [
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1],
        ],
        dtype=int,
    ),
    "vaisseau leger": np.array(
        [
            [0, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0],
        ],
        dtype=int,
    ),
    "clignotant": np.array(
        [
            [1, 1, 1],
        ],
        dtype=int,
    ),
    "crapaud": np.array(
        [
            [0, 1, 1, 1],
            [1, 1, 1, 0],
        ],
        dtype=int,
    ),
    "balise": np.array(
        [
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 0, 1, 1],
        ],
        dtype=int,
    ),
    "pentadecathlon": np.array(
        [
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        ],
        dtype=int,
    ),
}


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
