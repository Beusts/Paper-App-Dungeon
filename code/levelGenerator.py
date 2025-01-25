import random
import csv
import os


def generate_maze(width, height):
    maze = [[0 for _ in range(width)] for _ in range(height)]
    divide(maze, 0, 0, width, height)
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


width, height = 13, 13
for _ in range(1):
    maze = generate_maze(width, height)

output_dir = 'data/levels'
os.makedirs(output_dir, exist_ok=True)

bordered_maze = [[1] * (width + 2)]
for row in maze:
    bordered_maze.append([1] + row + [1])
bordered_maze.append([1] * (width + 2))

player_x, player_y = 2, 2
bordered_maze[player_y][player_x] = 'P'

with open(os.path.join(output_dir, 'grid.csv'), 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(bordered_maze)
