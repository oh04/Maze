from collections import deque
import random

PRESETS = {
    "Easy": {
        "width": 8,
        "height": 6,
        "fog_enabled": False,
        "light_radius": 2,
        "show_revealed": True
    },
    "Medium": {
        "width": 13,
        "height": 9,
        "fog_enabled": True,
        "light_radius": 2,
        "show_revealed": True
    },
    "Hard": {
        "width": 18,
        "height": 12,
        "fog_enabled": True,
        "light_radius": 1,
        "show_revealed": True
    },
    "Impossible": {
        "width": 24,
        "height": 16,
        "fog_enabled": True,
        "light_radius": 1,
        "show_revealed": False
    }
}

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

    if exit_position not in came_from:
        return None

    path = []
    coord = exit_position
    while coord is not None:
        path.append(coord)
        coord = came_from[coord]

    path.reverse()
    return path

def light_diag(position, cell, radius=1):
    x, y = position
    i, j = cell
    dif_x = abs(x - i)
    dif_y = abs(y - j)
    if dif_x > radius or dif_y > radius:
        return 0
    elif dif_x == 0 and dif_y == 0:
        return 1
    elif dif_x == radius and dif_y == radius:
        return 0.5
    else:
        return 1

def get_diff(difficulty, custom=None):
    if difficulty == "Custom":
        if custom is None:
            raise ValueError
        diff = custom.copy()
    elif difficulty in PRESETS:
        diff = PRESETS[difficulty].copy()
    else:
        raise ValueError
    diff["difficulty"] = difficulty
    return diff

def stats():
    return {
        "Easy": {
                    "wins": 0,
                    "give_ups": 0,
                    "avg_moves": None,
                    "avg_excess": None,
                    "best_excess": None,
                    "worst_excess": None
                },
        "Medium": {
                    "wins": 0,
                    "give_ups": 0,
                    "avg_moves": None,
                    "avg_excess": None,
                    "best_excess": None,
                    "worst_excess": None
                },
        "Hard": {
                    "wins": 0,
                    "give_ups": 0,
                    "avg_moves": None,
                    "avg_excess": None,
                    "best_excess": None,
                    "worst_excess": None
                },
        "Impossible": {
                    "wins": 0,
                    "give_ups": 0,
                    "avg_moves": None,
                    "avg_excess": None,
                    "best_excess": None,
                    "worst_excess": None
                }

    }

def record_results(stats, difficulty, won, moves, shortest_moves):
    if difficulty == "Custom":
        return
    record = stats[difficulty]
    if not won:
        record["give_ups"] += 1
        return
    excess = moves - shortest_moves
    record["wins"] += 1
    if record["best_excess"] is None:
        record["avg_moves"] = moves
        record["best_excess"] = excess
        record["worst_excess"] = excess
        record["avg_excess"] = excess
        return
    record["avg_moves"] = ((record["avg_moves"] * (record["wins"] - 1)) + moves) / record["wins"]
    record["avg_excess"] = ((record["avg_excess"] * (record["wins"] - 1)) + excess) / record["wins"]
    if excess < record["best_excess"]:
        record["best_excess"] = excess
    elif excess > record["worst_excess"]:
        record["worst_excess"] = excess