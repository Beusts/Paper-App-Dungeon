import random
from copyreg import constructor
from random import randint
import csv
import os


def create_maze_csv_file(name, width, height):
    maze, rooms = generate_maze(width, height)

    adding_objects_on_level(maze, rooms, width, height, 0.4)

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


def adding_objects_on_level(maze, rooms, width, height, object_percentage):
    current_object_position_on_level = having_current_object_position_on_level(maze)
    current_object_on_level = []

    # Place a player on the level
    coo_player = place_player_on_maze(rooms, current_object_position_on_level)

    # Place a stair on the level
    coo_stair = place_stair_on_maze(rooms, coo_player, current_object_position_on_level)

    current_object_on_level.append({"coo": coo_player, "symbol": "P"})
    current_object_on_level.append({"coo": coo_stair, "symbol": "S"})

    place_objects_on_rooms(rooms, current_object_position_on_level, current_object_on_level, object_percentage)


    for o in current_object_on_level:
        coo = o["coo"]
        if not coo: break
        symbol = o["symbol"]
        maze[coo[1]][coo[0]] = symbol

    return maze

def having_current_object_position_on_level(maze):
    objects_position = []
    row_id, col_id = 0, 0

    for row in maze:
        for col in row:
            if col != 0:
                objects_position.append((row_id, col_id))
            col_id += 1
        row_id += 1
        col_id = 0
    return objects_position

def place_player_on_maze(rooms, current_object_position_on_level):
    pos_x, pos_y, width, height = select_random_room(rooms)
    return generate_point(  (pos_x, pos_x + width), (pos_y, pos_y + height), current_object_position_on_level)

def place_stair_on_maze(rooms, coo_player, current_object_position_on_level):
    pos_x, pos_y, width, height = select_random_room(rooms)

    if not is_object_in_a_room(pos_x, pos_y, width, height, coo_player):
        return generate_point(  (pos_x, pos_x + width), (pos_y, pos_y + height), current_object_position_on_level)

    while is_object_in_a_room(pos_x, pos_y, width, height, coo_player):
        pos_x, pos_y, width, height = select_random_room(rooms)

    return generate_point(  (pos_x, pos_x + width), (pos_y, pos_y + height), current_object_position_on_level)


def place_objects_on_rooms(rooms, current_object_position_on_level, current_object_on_level, object_percentage):

    for room in rooms:
        start_x, start_y = room[0]
        end_x, end_y = room[1]
        width, height = abs(start_x - end_x), abs(start_y - end_y)
        room_max_objects = width * height * object_percentage

        # Place an object inside the rooms
        _object = generate_random_object(rooms, ((start_x, end_x), (start_y, end_y)),
                                         current_object_position_on_level, current_object_on_level)
        if not _object: return

        # Manage rooms
        if _object[0] == "C":  # If object is a chest, adding some enemies around it
            current_object_on_level.append({"coo": _object[1], "symbol": _object[0]})
            chest_room(start_x, start_y, width, height, room_max_objects, current_object_position_on_level,
                       current_object_on_level)
            continue

        if _object[0] == "T":
            have_teleporter = False
            for o in current_object_on_level:
                if "T" in o["symbol"]:
                    have_teleporter = True
                    break

            if have_teleporter: continue
            current_object_on_level.append({"coo": _object[1], "symbol": _object[0]})
            teleporters_room(rooms, start_x, start_y, current_object_position_on_level, current_object_on_level)
            continue

        for i in range(int(room_max_objects)):
            _object = generate_random_object(rooms, ((start_x, end_x), (start_y, end_y)),
                                             current_object_position_on_level, current_object_on_level)

            if not _object or _object[0] == "C" or _object[0] == "T":
                continue

            current_object_on_level.append({"coo": _object[1], "symbol": _object[0]})
    return

def chest_room(pos_x, pos_y, width, height, room_max_objects, current_object_position_on_level, current_object_on_level):
    for i in range(int(room_max_objects)):
        row_min_max = pos_x, pos_x + width
        col_min_max = pos_y, pos_y + height
        point = generate_point(row_min_max, col_min_max, current_object_position_on_level)

        malus_type = randint(1, 3)

        if malus_type == 1:  # Standart Enemy
            value = randint(1, 6)
            symbol = "Se" + str(value)
            current_object_on_level.append({"coo": point, "symbol": symbol})

        if malus_type == 2:  # Mystery Enemy
            current_object_on_level.append({"coo": point, "symbol": "Me"})

        if malus_type == 3:
            current_object_on_level.append({"coo": point, "symbol": "W"})

    return

def teleporters_room(rooms, pos_x, pos_y, current_object_position_on_level, current_object_on_level):
    print(f"old room : {pos_x, pos_y}")

    # Find another room to put another teleporter
    new_pos_x, new_pos_y, width, height = select_random_room(rooms)

    while new_pos_x == pos_x and new_pos_y == pos_y:
        new_pos_x, new_pos_y, width, height = select_random_room(rooms)

    print(f"new room : {new_pos_x, new_pos_y}")

    row_min_max = new_pos_x, new_pos_x + width
    col_min_max = new_pos_y, new_pos_y + height
    point = generate_point(row_min_max, col_min_max, current_object_position_on_level)
    current_object_on_level.append({"coo": point, "symbol": "T"})

def generate_random_object(rooms, borne, current_object_position_on_level, current_object_on_level):
    object_id = randint(1, 8)
    row_min_max = borne[0]
    col_min_max = borne[1]

    new_room = []
    point = generate_point(  row_min_max, col_min_max, current_object_position_on_level)
    if not point: return False

    symbol = ""

    if object_id == 1:  # Standart Enemy
        value = randint(1, 6)
        symbol = "Se" + str(value)

    if object_id == 2:  # Mystery Enemy
        symbol = "Me"

    if object_id == 3:  # Standart Heart
        value = randint(1, 6)
        symbol = "Sh" + str(value)

    if object_id == 4:  # Mystery Heart
        symbol = "Mh"

    if object_id == 5:  # Coin
        symbol = "Co"

    if object_id == 6:  # Chest
        symbol = "C"

    if object_id == 7:  # spiderWeb
        symbol = "W"

    if object_id == 8:  # Teleporter
        symbol = "T"

    return symbol, point

def generate_point( row_min_max, col_min_max, current_object_position_on_level):

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


def select_random_room(rooms):
    room_id = randint(0, len(rooms) - 1)
    current_room = rooms[room_id]
    return calculate_size_room(current_room)

def calculate_size_room(room):
    first_x, first_y = room[0]
    last_x, last_y = room[1]
    return first_x, first_y, abs(first_x - last_x), abs(first_y - last_y)

def is_object_in_a_room(pos_x, pos_y, width, height, coo):
    in_x = pos_x <= coo[0] <= pos_x + width
    in_y = pos_y <= coo[1] <= pos_y + height

    return in_x and in_y




