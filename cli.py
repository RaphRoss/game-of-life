import argparse


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
