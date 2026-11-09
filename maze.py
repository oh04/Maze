import random

def main():
    print()

maze = ["#######", "#S#...#", "#.#.#E#", "#...#.#", "#######",]

def is_walkable(maze, x, y):
    if 0 <= x <= len(maze) - 1 and 0 <= y <= len(maze[x]) - 1:
        return maze[x][y] in ".SE"
    return False

def has_won(maze, position):
    return position == (len(maze) - 1, len(maze[0]) - 1)

def generate_maze(width, height):
    grid = create_grid(height, width)
    stack = [(0, 0)]
    visited = {(0, 0)}
    while stack:
        x, y = stack[-1]
        neighbors = unvisited_neighbors(grid, stack[-1], visited)
        if not neighbors:
            stack.pop()
            continue
        new_x, new_y = random.choice(neighbors)
        remove_wall(grid, (x, y), (new_x, new_y))
        visited.add((new_x, new_y))
        stack.append((new_x, new_y))
    return grid

def unvisited_neighbors(grid, position, visited):
    x, y = position
    neighbors = []
    for x_change, y_change in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x = x + x_change
        new_y = y + y_change
        if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and (new_x, new_y) not in visited:
            neighbors.append((new_x, new_y))
    return neighbors

def create_grid(height, width):
    grid = [[{"north": True, "south": True, "east": True, "west": True} for _ in range(height)] for _ in range(width)]
    return grid

def remove_wall(grid, first, second):
    x1, y1 = first
    x2, y2 = second
    if x1 > x2:
        grid[x1][y1]["west"] = False
        grid[x2][y2]["east"] = False
    elif x1 < x2:
        grid[x1][y1]["east"] = False
        grid[x2][y2]["west"] = False
    elif y1 > y2:
        grid[x1][y1]["north"] = False
        grid[x2][y2]["south"] = False
    elif y1 < y2:
        grid[x1][y1]["south"] = False
        grid[x2][y2]["north"] = False

def try_move(grid, position, direction):
    x, y = position
    dirX, dirY = direction
    new_x = x + dirX
    new_y = y + dirY
    if dirX == 1:
        move = "east"
    elif dirX == -1:
        move = "west"
    elif dirY == 1:
        move = "south"
    elif dirY == -1:
        move = "north"
    if 0 <= new_x <= len(grid) - 1 and 0 <= new_y <= len(grid[x]) - 1 and not grid[x][y][move]:
        return (new_x, new_y)
    return position