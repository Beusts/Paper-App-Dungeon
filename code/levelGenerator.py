import random
from random import randint
import csv
import os



def generate_maze(width, height):
    maze = [[0 for _ in range(width)] for _ in range(height)]
    divide(maze, 0, 0, width, height)

    adding_objects_on_level(maze, width, height, 0.06)
    return maze

def divide(maze, x, y, width, height):
    if width < 5 or height < 5:
        return

    if width == height:
        if random.choice([True, False]):
            divide_vertically(maze, x, y, width, height)
        else:
            divide_horizontally(maze, x, y, width, height)
    elif width > height:
        divide_vertically(maze, x, y, width, height)
    else:
        divide_horizontally(maze, x, y, width, height)


def divide_vertically(maze, x, y, width, height):
    wx = x + random.randint(2, width - 3)
    for i in range(y, y + height):
        maze[i][wx] = 1
    passage = y + random.randint(0, height - 3)
    maze[passage][wx] = 0
    maze[passage + 1][wx] = 0
    divide(maze, x, y, wx - x, height)
    divide(maze, wx + 2, y, x + width - wx - 2, height)


def divide_horizontally(maze, x, y, width, height):
    wy = y + random.randint(2, height - 3)
    for i in range(x, x + width):
        maze[wy][i] = 1
    passage = x + random.randint(0, width - 3)
    maze[wy][passage] = 0
    maze[wy][passage + 1] = 0
    divide(maze, x, y, width, wy - y)
    divide(maze, x, wy + 2, width, y + height - wy - 2)



def adding_objects_on_level(maze, witdh, height, object_pourcentage):

    current_object_position_on_level = having_current_object_position_on_level(maze)
    current_object_on_level = []

    size_level = witdh * height
    max_objects = size_level * object_pourcentage

    # Place a player on the level
    coo_player = generate_point((1, witdh - 2), (1, height - 2), current_object_position_on_level)

    # Place a stair on the level
    coo_stair = generate_point((1, witdh - 2), (1, height - 2), current_object_position_on_level)

    current_object_on_level.append({"coo": coo_player, "symbol": "P"})
    current_object_on_level.append({"coo": coo_stair, "symbol": "S"})
    object_count = 2

    while object_count < max_objects:
        _object = generate_random_object(current_object_position_on_level, witdh, height)

        for o in _object:
            print(o)
            current_object_on_level.append(o)
            object_count += 1


    for o in current_object_on_level:
        coo = o["coo"]
        symbol = o["symbol"]
        print(f"coo : {coo}, symbol : {symbol}")
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
        return [{"coo": generate_point((1, witdh - 2) ,(1, height - 2), current_object_position_on_level), "symbol": symbol}]

    if object_id == 2:  # Mystery Enemy
        return [{"coo": generate_point((1, witdh - 2), (1, height - 2), current_object_position_on_level), "symbol": "Me"}]

    if object_id == 3:  # Standart Heart
        value = randint(1, 6)
        symbol = "Sh" + str(value)
        return [{"coo": generate_point((1, witdh - 2), (1, height - 2), current_object_position_on_level), "symbol": symbol}]

    if object_id == 4:  # Mystery Heart
        return [{"coo": generate_point((1, witdh - 2), (1, height - 2), current_object_position_on_level), "symbol": "Me"}]

    if object_id == 5:  # Coin
        return [{"coo": generate_point((1, witdh - 2),(1, height - 2),  current_object_position_on_level), "symbol": "Co"}]

    if object_id == 6:  # Chest
        return [{"coo": generate_point((1, witdh - 2),(1, height - 2),  current_object_position_on_level), "symbol": "C"}]

    if object_id == 7:  # spiderWeb
        return [{"coo": generate_point((1, witdh - 2), (1, height - 2), current_object_position_on_level), "symbol": "W"}]

    if object_id == 8:  # Teleporter
        t1 = generate_point((1, witdh - 2), (1, height - 2), current_object_position_on_level)
        t2 = generate_point((1, witdh - 2), (1, height - 2), current_object_position_on_level)

        print(f"teleporters : {t1}, {t2}")

        return  [{"coo": t1, "symbol": "T"}, {"coo": t2, "symbol": "T"}]


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

    for _ in range(1):
        maze = generate_maze(width, height)

    print(maze)

    output_dir = 'data/levels'
    os.makedirs(output_dir, exist_ok=True)

    bordered_maze = [[1] * (width + 2)]

    for row in maze:
        bordered_maze.append([1] + row + [1])
    bordered_maze.append([1] * (width + 2))

    player_x, player_y = 2, 2
    bordered_maze[player_y][player_x] = 'P'

    with open(os.path.join(output_dir, f'{name}.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(bordered_maze)
