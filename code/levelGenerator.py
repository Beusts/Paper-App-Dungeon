"""
Module pour la génération procédurale des niveaux sous forme de labyrinthes.
Ce module contient des fonctions pour créer des niveaux de jeu sous forme de fichiers CSV.
"""

import random
from random import randint
import csv
import os


def stock_steps(maze):
    global name_step
    output_dir = os.path.join('data', 'levels', f'{name_step}_steps')
    os.makedirs(output_dir, exist_ok=True)

    global step
    step += 1
    with open(os.path.join(output_dir, f'{step}.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(maze)


def load_generation_steps(name):
    """
    Charge les étapes de génération d'un labyrinthe à partir des fichiers CSV.

    Args:
        name (str): Nom du niveau pour lequel charger les étapes

    Returns:
        list: Liste des matrices représentant chaque étape de la génération
    """
    steps = []
    steps_dir = os.path.join('data', 'levels', f'{name}_steps')

    if not os.path.exists(steps_dir):
        return steps

    step_files = [f for f in os.listdir(steps_dir) if f.endswith('.csv')]
    step_files.sort(key=lambda x: int(x.split('.')[0]))

    for step_file in step_files:
        with open(os.path.join(steps_dir, step_file), newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            maze_step = list(reader)
            steps.append(maze_step)

    return steps


def create_maze_csv_file(name, width, height, difficulty=1):
    """
    Crée un fichier CSV représentant un niveau de labyrinthe.

    Args:
        name (str): Nom du fichier à créer (sans extension)
        width (int): Largeur du labyrinthe
        height (int): Hauteur du labyrinthe
        difficulty (int, optional): Niveau de difficulté du labyrinthe. Défaut à 1.
    """
    global name_step
    name_step = name

    output_dir = os.path.join('data', 'levels', f'{name_step}_steps')
    if os.path.exists(output_dir):
        for file in os.listdir(output_dir):
            os.remove(os.path.join(output_dir, file))
        os.rmdir(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    maze, rooms = generate_maze(width, height, name)
    apply_room_template(maze, rooms, difficulty)

    output_dir = os.path.join('data', 'levels')
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, f'{name}.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(maze)


def generate_maze(width, height, name):
    """
    Génère un labyrinthe avec des salles.

    Args:
        width (int): Largeur du labyrinthe
        height (int): Hauteur du labyrinthe

    Returns:
        tuple: (maze, rooms) où maze est une matrice du labyrinthe et rooms est la liste des salles
    """
    maze = [[0 for _ in range(width)] for _ in range(height)]
    rooms = []

    topLeft = (1, 1)
    bottomRight = (width - 2, height - 2)

    global step
    step = 0

    divide(maze, topLeft, bottomRight, rooms)

    for i in range(width):
        maze[0][i] = 1
        maze[height - 1][i] = 1
    for i in range(height):
        maze[i][0] = 1
        maze[i][width - 1] = 1
    stock_steps(maze)

    return maze, rooms


def chooseOrientation(width, height):
    """
    Détermine l'orientation d'un mur dans le labyrinthe.

    Args:
        width (int): Largeur de la section
        height (int): Hauteur de la section

    Returns:
        bool: True pour orientation verticale, False pour horizontale
    """

    if width < height:
        return True
    elif height < width:
        return False
    else:
        return random.choice([True, False])


def addWall(walls, startPoint, endPoint, doorIdx, orientation):
    """
    Ajoute un mur avec une porte dans le labyrinthe.

    Args:
        walls (list): Matrice du labyrinthe
        startPoint (tuple): Point de départ du mur (x, y)
        endPoint (tuple): Point d'arrivée du mur (x, y)
        doorIdx (tuple): Position de la porte (x, y)
        orientation (bool): True pour mur vertical, False pour horizontal
    """
    if orientation == True:
        for x in range(0, endPoint[0] - startPoint[0] + 1):
            walls[startPoint[1]][startPoint[0] + x] = 1
        stock_steps(walls)
        walls[doorIdx[0]][doorIdx[1]] = 0
        walls[doorIdx[0]][doorIdx[1] + 1] = 0
        stock_steps(walls)
    else:
        for y in range(0, endPoint[1] - startPoint[1] + 1):
            walls[startPoint[1] + y][startPoint[0]] = 1
        stock_steps(walls)
        walls[doorIdx[0]][doorIdx[1]] = 0
        walls[doorIdx[0] + 1][doorIdx[1]] = 0
        stock_steps(walls)


def divide(walls, topLeft, bottomRight, rooms):
    """
    Divise récursivement un espace pour créer un labyrinthe.

    Args:
        walls (list): Matrice du labyrinthe
        topLeft (tuple): Coin supérieur gauche de l'espace à diviser (x, y)
        bottomRight (tuple): Coin inférieur droit de l'espace à diviser (x, y)
        rooms (list): Liste des salles du labyrinthe
    """
    possibleRows = []
    possibleCols = []

    orientation = chooseOrientation(
        bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1])

    if orientation == True:
        for i in range(topLeft[1] + 2, bottomRight[1] - 1):
            possibleRows.append(i)
        for i in range(topLeft[0], bottomRight[0]):
            possibleCols.append(i)

        wallY = random.choice(possibleRows)
        door = (wallY, random.choice(possibleCols))

        addWall(walls, (topLeft[0], wallY),
                (bottomRight[0], wallY), door, orientation)

        newTopLeft = topLeft
        newBottomRight = (bottomRight[0], wallY - 1)

        if (newBottomRight[0] - newTopLeft[0] + 1) * (newBottomRight[1] - newTopLeft[1] + 1) >= 26:
            divide(walls, newTopLeft, newBottomRight, rooms)
        else:
            rooms.append(
                (topLeft, (bottomRight[0], wallY - 1), (door, (door[0], door[1] + 1)), []))

        newTopLeft = (topLeft[0], wallY + 1)
        newBottomRight = bottomRight

        if (newBottomRight[0] - newTopLeft[0] + 1) * (newBottomRight[1] - newTopLeft[1] + 1) >= 26:
            divide(walls, newTopLeft, newBottomRight, rooms)
        else:
            rooms.append((newTopLeft, newBottomRight,
                         (door, (door[0], door[1] + 1)), []))
    else:
        for i in range(topLeft[0] + 2, bottomRight[0] - 1):
            possibleCols.append(i)
        for i in range(topLeft[1], bottomRight[1]):
            possibleRows.append(i)

        wallX = random.choice(possibleCols)
        door = (random.choice(possibleRows), wallX)

        addWall(walls, (wallX, topLeft[1]),
                (wallX, bottomRight[1]), door, orientation)

        newTopLeft = topLeft
        newBottomRight = (wallX - 1, bottomRight[1])

        if (newBottomRight[0] - newTopLeft[0] + 1) * (newBottomRight[1] - newTopLeft[1] + 1) >= 26:
            divide(walls, topLeft, (wallX - 1, bottomRight[1]), rooms)
        else:
            rooms.append(
                (topLeft, (wallX - 1, bottomRight[1]), (door, (door[0] + 1, door[1])), []))

        newTopLeft = (wallX + 1, topLeft[1])
        newBottomRight = bottomRight

        if (newBottomRight[0] - newTopLeft[0] + 1) * (newBottomRight[1] - newTopLeft[1] + 1) >= 26:
            divide(walls, (wallX + 1, topLeft[1]), bottomRight, rooms)
        else:
            rooms.append(
                ((wallX + 1, topLeft[1]), bottomRight, (door, (door[0] + 1, door[1])), []))


def apply_room_template(maze, rooms, difficulty):
    """
    Applique des modèles aux salles du labyrinthe pour y ajouter des objets et ennemis.

    Args:
        maze (list): Matrice du labyrinthe
        rooms (list): Liste des salles du labyrinthe
        difficulty (int): Niveau de difficulté du labyrinthe
    """
    templates = [
        {"func": template_base_room, "weight": 1, "max_count": None},
        {"func": template_chest_room, "weight": 9, "max_count": 1},
        {"func": template_teleporters_room, "weight": 2, "max_count": 1}
    ]
    template_counts = {template["func"]: 0 for template in templates}

    for room in rooms:
        available_templates = [
            t for t in templates if t["max_count"] is None or template_counts[t["func"]] < t["max_count"]]
        if not available_templates:
            break
        weights = [t["weight"] for t in available_templates]
        while available_templates:
            chosen_template = random.choices(available_templates, weights)[0]
            if chosen_template["func"](maze, room, rooms, difficulty):
                template_counts[chosen_template["func"]] += 1
                break
            else:
                available_templates.remove(chosen_template)
                weights = [t["weight"] for t in available_templates]

    player_room = random.choice([room for room in rooms if "C" not in [
                                maze[y][x] for x, y in room[3]]])

    player_point = generate_point(player_room)
    if player_point:
        maze[player_point[1]][player_point[0]] = "P"

    stair_room = random.choice([room for room in rooms if room != player_room])
    stair_point = generate_point(stair_room)
    if stair_point:
        maze[stair_point[1]][stair_point[0]] = "S"


def template_base_room(maze, room, rooms, difficulty):
    """
    Applique un modèle de base à une salle avec des ennemis et objets générés aléatoirement.

    Args:
        maze (list): Matrice du labyrinthe
        room (tuple): Informations sur la salle
        rooms (list): Liste des salles du labyrinthe
        difficulty (int): Niveau de difficulté

    Returns:
        bool: True si le modèle a été appliqué avec succès
    """
    start_x, start_y = room[0]
    end_x, end_y = room[1]
    width, height = abs(start_x - end_x) + 1, abs(start_y - end_y) + 1
    max_objects = int((width * height) * 0.2)

    symbols = [
        # Standart Enemy
        lambda: f"Se{randint(1 * difficulty, 6 + int(difficulty / 2))}",
        lambda: "Me",  # Mystery Enemy
        lambda: f"Sh{randint(1, 6)}",  # Standart Heart
        lambda: "Mh",  # Mystery Heart
        lambda: "Co",  # Coin
        lambda: "C",  # Chest
        lambda: "W",  # SpiderWeb
    ]
    for _ in range(max_objects):
        object_id = randint(0, len(symbols) - 1)
        symbol = symbols[object_id]()
        point = generate_point(room)
        if point:
            maze[point[1]][point[0]] = symbol
    return True


def template_chest_room(maze, room, rooms, difficulty):
    """
    Applique un modèle de salle au trésor avec un porte verrouillé.

    Args:
        maze (list): Matrice du labyrinthe
        room (tuple): Informations sur la salle
        rooms (list): Liste des salles du labyrinthe
        difficulty (int): Niveau de difficulté

    Returns:
        bool: True si le modèle a été appliqué avec succès
    """
    start_x, start_y = room[0]
    end_x, end_y = room[1]
    width, height = abs(start_x - end_x) + 1, abs(start_y - end_y) + 1
    max_objects = int((width * height) * 0.2)

    for i in range(start_x - 1, end_x + 2):
        if ((maze[start_y - 1][i] != 1 and not (start_y - 1, i) in room[2]) or (maze[end_y + 1][i] != 1) and not (end_y + 1, i) in room[2]):
            return False
    for j in range(start_y - 1, end_y + 2):
        if ((maze[j][start_x - 1] != 1 and not (j, start_x - 1) in room[2]) or (maze[j][end_x + 1] != 1) and not (j, end_x + 1) in room[2]):
            return False

    point = generate_point(room)
    if point:
        maze[point[1]][point[0]] = "C"

    for i in range(start_x, end_x + 1):
        for j in range(start_y, end_y + 1):
            if maze[j][i] == 0 and (0 == randint(0, 2)):
                maze[j][i] = "Co"

    maze[room[2][0][0]][room[2][0][1]] = "L"
    maze[room[2][1][0]][room[2][1][1]] = "1"

    key_room = random.choice([r for r in rooms if r != room])
    key_point = generate_point(key_room)
    if key_point:
        maze[key_point[1]][key_point[0]] = "K"

    return True


def template_teleporters_room(maze, room_teleporter_1, rooms, difficulty):
    """
    Applique un modèle de salle avec téléporteurs.

    Args:
        maze (list): Matrice du labyrinthe
        room_teleporter_1 (tuple): Informations sur la première salle avec téléporteur
        rooms (list): Liste des salles du labyrinthe
        difficulty (int): Niveau de difficulté

    Returns:
        bool: True si le modèle a été appliqué avec succès
    """
    room_teleporter_2 = random.choice(
        [r for r in rooms if r != room_teleporter_1])
    symbol_teleporters = "T"

    point_teleporter_1 = generate_point(room_teleporter_1)
    point_teleporter_2 = generate_point(room_teleporter_2)

    if not point_teleporter_1 or not point_teleporter_2:
        return False

    maze[point_teleporter_1[1]][point_teleporter_1[0]] = symbol_teleporters
    maze[point_teleporter_2[1]][point_teleporter_2[0]] = symbol_teleporters

    return template_base_room(maze, room_teleporter_1, rooms, difficulty)


def generate_point(room):
    """
    Génère un point aléatoire dans une salle qui n'est pas déjà occupé.

    Args:
        room (tuple): Informations sur la salle

    Returns:
        tuple: Coordonnées (x, y) du point généré ou None si aucun espace n'est disponible
    """
    available_points = [(x, y) for x in range(room[0][0], room[1][0] + 1)
                        for y in range(room[0][1], room[1][1] + 1) if (x, y) not in room[3]]
    if not available_points:
        return None
    point = random.choice(available_points)
    room[3].append(point)
    return point
