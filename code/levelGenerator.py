import random
import csv
import os


def generate_maze(width, height):
    maze = [[0 for _ in range(width)] for _ in range(height)]
    divide(maze, 0, 0, width, height)
    return maze


def divide(maze, x, y, width, height):
    if width <= 4 or height <= 4:
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
    wx = x + random.randint(1, width - 2)
    for i in range(y, y + height):
        maze[i][wx] = 1
    passage = y + random.randint(0, height - 2)
    maze[passage][wx] = 0
    maze[passage + 1][wx] = 0
    divide(maze, x, y, wx - x, height)
    divide(maze, wx + 1, y, x + width - wx - 1, height)


def divide_horizontally(maze, x, y, width, height):
    wy = y + random.randint(1, height - 2)
    for i in range(x, x + width):
        maze[wy][i] = 1
    passage = x + random.randint(0, width - 2)
    maze[wy][passage] = 0
    maze[wy][passage + 1] = 0
    divide(maze, x, y, width, wy - y)
    divide(maze, x, wy + 1, width, y + height - wy - 1)


# Exemple d'utilisation
width, height = 15, 15
for _ in range(1):
    maze = generate_maze(width, height)

for i in range(width):
    maze[0][i] = 1
    maze[height - 1][i] = 1
for i in range(height):
    maze[i][0] = 1
    maze[i][width - 1] = 1

output_dir = 'data/levels'
os.makedirs(output_dir, exist_ok=True)

with open(os.path.join(output_dir, 'grid.csv'), 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(maze)
