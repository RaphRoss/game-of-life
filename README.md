# Jeu de la Vie (Conway)

Simulation console du Jeu de la Vie en Python avec:
- taille de grille configurable
- nombre de cycles configurable
- detection de motifs connus
- resume statistique en fin de partie

## Prerequis

- Python 3
- `numpy`

## Installation rapide

```bash
python3 -m venv venv
source venv/bin/activate
pip install numpy
```

## Lancement

### Valeurs par defaut

```bash
python3 life_game.py
```

### Choisir la taille de grille

```bash
python3 life_game.py 30
```

### Choisir la taille et le nombre de cycles

```bash
python3 life_game.py 30 --cycles 250
```

Option courte:

```bash
python3 life_game.py 30 -c 250
```

## Aide

```bash
python3 life_game.py -h
```

## Statistiques de fin

A la fin de la simulation, le programme affiche:
- nb de cellule immortel
- nb de cellule cree
- nb de cellule morte

Puis des exemples de types detectes avec leur compteur, affiches cote a cote (ex: `cellule voyageur cree : X` et `clignotant cree : Y`).

## Motifs detectes (actuellement)

- Stables: bloc stable, ruche, pain, bateau, bassine
- Oscillateurs: clignotant, crapaud, balise, pentadecathlon
- Vaisseaux: cellule voyageur, vaisseau leger

## Structure du projet

- `life_game.py`: point d'entree principal
- `cli.py`: gestion des arguments (`size`, `--cycles`)
- `simulation.py`: logique de simulation et detection
- `patterns.py`: bibliotheque de motifs
- `display.py`: affichage grille + resume final
