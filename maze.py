from collections import deque
import random

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

def visible_squares(grid, position, radius=1):
    x, y = position
    visible = set()
    for try_x in range(x - radius, x + radius + 1):
        for try_y in range(y - radius, y + radius + 1):
            if 0 <= try_x <= len(grid) - 1 and 0 <= try_y <= len(grid[0]) - 1:
                visible.add((try_x, try_y))
    return visible

def shortest_path(grid, start, exit_position):
    q = deque()
    q.append(start)
    visited = {start}
    came_from = {start: None}

    while q:
        current = q.popleft()
        for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            neighbor = try_move(grid, current, direction)
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
                came_from[neighbor] = current

    if not exit_position in came_from:
        return None

    path = list()
    coord = exit_position
    while coord != None:
        path.append(coord)
        coord = came_from[coord]

    path.reverse()
    return path