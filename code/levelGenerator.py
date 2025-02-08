import random
from copyreg import constructor
from os import pread
from random import randint
import csv
import os

def create_maze_csv_file(name, width, height, difficulty = 1):
    maze, rooms = generate_maze(width, height)
    apply_room_template(maze, rooms, difficulty)

    output_dir = 'data/levels'
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, f'{name}.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(maze)


def generate_maze(width, height):
    maze = [[0 for _ in range(width)] for _ in range(height)]
    rooms = []

    topLeft = (1, 1)
    bottomRight = (width - 2, height - 2)
    seed = random.random()
    random.seed(seed)
    print(seed)

    divide(maze, topLeft, bottomRight, rooms)

    for i in range(width):
        maze[0][i] = 1
        maze[height - 1][i] = 1
    for i in range(height):
        maze[i][0] = 1
        maze[i][width - 1] = 1

    return maze, rooms


def chooseOrientation(width, height):
    """
    Horizontal = False
    Vertical = True
    """

    if width < height:
        return True
    elif height < width:
        return False
    else:
        return random.choice([True, False])


def addWall(walls, startPoint, endPoint, doorIdx, orientation):
    if orientation == True:
        for x in range(0, endPoint[0] - startPoint[0] + 1):
            walls[startPoint[1]][startPoint[0] + x] = 1
        walls[doorIdx[0]][doorIdx[1]] = 0
        walls[doorIdx[0]][doorIdx[1] + 1] = 0
    else:
        for y in range(0, endPoint[1] - startPoint[1] + 1):
            walls[startPoint[1] + y][startPoint[0]] = 1
        walls[doorIdx[0]][doorIdx[1]] = 0
        walls[doorIdx[0] + 1][doorIdx[1]] = 0


def divide(walls, topLeft, bottomRight, rooms):
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

    player_room = random.choice(rooms)
    player_point = generate_point(player_room)
    if player_point:
        maze[player_point[1]][player_point[0]] = "P"

    stair_room = random.choice([room for room in rooms if room != player_room])
    stair_point = generate_point(stair_room)
    if stair_point:
        maze[stair_point[1]][stair_point[0]] = "S"


def template_base_room(maze, room, rooms, difficulty):
    start_x, start_y = room[0]
    end_x, end_y = room[1]
    width, height = abs(start_x - end_x) + 1, abs(start_y - end_y) + 1
    max_objects = int((width * height) * 0.2)

    symbols = [
        lambda: f"Se{randint(1 * difficulty, 6 + int(difficulty / 2))}",  # Standart Enemy
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

def template_teleporters_room(maze, room_teleporter_1, rooms, difficulty) :
    room_teleporter_2 = random.choice([r for r in rooms if r != room_teleporter_1])
    symbol_teleporters = "T"

    point_teleporter_1 = generate_point(room_teleporter_1)
    point_teleporter_2 = generate_point(room_teleporter_2)

    if not point_teleporter_1 or not point_teleporter_2:
        return False

    maze[point_teleporter_1[1]][point_teleporter_1[0]] = symbol_teleporters
    maze[point_teleporter_2[1]][point_teleporter_2[0]] = symbol_teleporters

    return template_base_room(maze, room_teleporter_1, rooms, difficulty)

def generate_point(room):
    attempts = 0
    max_attempts = 100
    while attempts < max_attempts:
        pos_x = randint(room[0][0], room[1][0])
        pos_y = randint(room[0][1], room[1][1])
        if (pos_x, pos_y) not in room[3]:
            room[3].append((pos_x, pos_y))
            return pos_x, pos_y
        attempts += 1
    return None

