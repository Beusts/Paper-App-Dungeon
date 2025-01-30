import random
from random import randint
import csv
import os


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

    adding_objects_on_level(maze, width, height, 0.06)
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
    if (bottomRight[0] - topLeft[0] + 1) * (bottomRight[1] - topLeft[1] + 1) < 26:
        rooms.append((topLeft, bottomRight))
        return

    possibleRows = []
    possibleCols = []

    orientation = chooseOrientation(
        bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1])

    if orientation == True:
        for i in range(topLeft[1] + 2, bottomRight[1] - 1):
            possibleRows.append(i)
        for i in range(topLeft[0], bottomRight[0]):
            possibleCols.append(i)

        if len(possibleCols) == 0 or len(possibleRows) == 0:
            rooms.append((topLeft, bottomRight))
            return

        wallY = random.choice(possibleRows)
        door = (wallY, random.choice(possibleCols))

        addWall(walls, (topLeft[0], wallY),
                (bottomRight[0], wallY), door, orientation)

        divide(walls, topLeft, (bottomRight[0], wallY - 1), rooms)
        divide(walls, (topLeft[0], wallY + 1), bottomRight, rooms)
    else:
        for i in range(topLeft[0] + 2, bottomRight[0] - 1):
            possibleCols.append(i)
        for i in range(topLeft[1], bottomRight[1]):
            possibleRows.append(i)

        if len(possibleCols) == 0 or len(possibleRows) == 0:
            rooms.append((topLeft, bottomRight))
            return

        wallX = random.choice(possibleCols)
        door = (random.choice(possibleRows), wallX)

        addWall(walls, (wallX, topLeft[1]),
                (wallX, bottomRight[1]), door, orientation)

        divide(walls, topLeft, (wallX - 1, bottomRight[1]), rooms)
        divide(walls, (wallX + 1, topLeft[1]), bottomRight, rooms)


def adding_objects_on_level(maze, witdh, height, object_pourcentage):
    current_object_position_on_level = having_current_object_position_on_level(
        maze)
    current_object_on_level = []

    size_level = witdh * height
    max_objects = size_level * object_pourcentage

    # Place a player on the level
    coo_player = generate_point(
        (1, witdh - 2), (1, height - 2), current_object_position_on_level)

    # Place a stair on the level
    coo_stair = generate_point(
        (1, witdh - 2), (1, height - 2), current_object_position_on_level)

    current_object_on_level.append({"coo": coo_player, "symbol": "P"})
    current_object_on_level.append({"coo": coo_stair, "symbol": "S"})
    object_count = 2

    while object_count < max_objects:
        _object = generate_random_object(
            current_object_position_on_level, witdh, height)

        for o in _object:
            current_object_on_level.append(o)
            object_count += 1

    for o in current_object_on_level:
        coo = o["coo"]
        symbol = o["symbol"]
        maze[coo[0]][coo[1]] = symbol

    return maze


def having_current_object_position_on_level(maze):
    objects_position = []
    for row in maze:
        for col in row:
            if col != 0:
                objects_position.append((row, col))

    return objects_position


def generate_random_object(current_object_position_on_level, witdh, height):
    object_id = randint(1, 8)

    if object_id == 1:  # Standart Enemy
        value = randint(1, 6)
        symbol = "Se" + str(value)
        return [{"coo": generate_point((1, witdh - 2), (1, height - 2), current_object_position_on_level), "symbol": symbol}]

    if object_id == 2:  # Mystery Enemy
        return [{"coo": generate_point((1, witdh - 2), (1, height - 2), current_object_position_on_level), "symbol": "Me"}]

    if object_id == 3:  # Standart Heart
        value = randint(1, 6)
        symbol = "Sh" + str(value)
        return [{"coo": generate_point((1, witdh - 2), (1, height - 2), current_object_position_on_level), "symbol": symbol}]

    if object_id == 4:  # Mystery Heart
        return [{"coo": generate_point((1, witdh - 2), (1, height - 2), current_object_position_on_level), "symbol": "Me"}]

    if object_id == 5:  # Coin
        return [{"coo": generate_point((1, witdh - 2), (1, height - 2),  current_object_position_on_level), "symbol": "Co"}]

    if object_id == 6:  # Chest
        return [{"coo": generate_point((1, witdh - 2), (1, height - 2),  current_object_position_on_level), "symbol": "C"}]

    if object_id == 7:  # spiderWeb
        return [{"coo": generate_point((1, witdh - 2), (1, height - 2), current_object_position_on_level), "symbol": "W"}]

    if object_id == 8:  # Teleporter
        t1 = generate_point((1, witdh - 2), (1, height - 2),
                            current_object_position_on_level)
        t2 = generate_point((1, witdh - 2), (1, height - 2),
                            current_object_position_on_level)

        return [{"coo": t1, "symbol": "T"}, {"coo": t2, "symbol": "T"}]


def generate_point(row_min_max, col_min_max, current_object_position_on_level):

    row = randint(row_min_max[0], row_min_max[1])
    col = randint(col_min_max[0], col_min_max[1])
    point = (row, col)

    if point not in current_object_position_on_level:
        current_object_position_on_level.append(point)
        return point

    while point in current_object_position_on_level:
        row = randint(row_min_max[0], row_min_max[1])
        col = randint(col_min_max[0], col_min_max[1])
        point = (row, col)

    current_object_position_on_level.append(point)
    return point


def create_maze_csv_file(name, width, height):
    maze, rooms = generate_maze(width, height)

    output_dir = 'data/levels'
    os.makedirs(output_dir, exist_ok=True)

    player_x, player_y = 2, 2
    maze[player_y][player_x] = 'P'

    with open(os.path.join(output_dir, f'{name}.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(maze)
