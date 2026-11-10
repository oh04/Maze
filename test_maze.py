from maze import create_grid, remove_wall, try_move

grid = create_grid(height=3, width=4)
assert len(grid) == 4
assert all(len(column) == 3 for column in grid)
assert all(
    cell == {"north": True, "south": True, "east": True, "west": True}
    for row in grid for cell in row
)
assert len({id(cell) for row in grid for cell in row}) == 12, "Each cell needs its own dictionary"

# closed walls block movement, openings must work in both directions
for direction, destination, wall, opposite in [
    ((-1, 0), (0, 1), "west", "east"),
    ((1, 0), (2, 1), "east", "west"),
    ((0, -1), (1, 0), "north", "south"),
    ((0, 1), (1, 2), "south", "north"),
]:
    grid = create_grid(height=3, width=4)
    assert try_move(grid, (1, 1), direction) == (1, 1)
    remove_wall(grid, (1, 1), destination)
    assert grid[1][1][wall] is False
    assert grid[destination[0]][destination[1]][opposite] is False
    reverse = (-direction[0], -direction[1])
    assert try_move(grid, (1, 1), direction) == destination
    assert try_move(grid, destination, reverse) == (1, 1)
    assert sum(value is False for row in grid for cell in row for value in cell.values()) == 2

# reopening a passage is harmless.
remove_wall(grid, (1, 1), (1, 2))
assert try_move(grid, (1, 1), (0, 1)) == (1, 2)

# Bounds protect movement even if an outer wall is accidentally absent.
grid = create_grid(height=3, width=4)
for position, direction, wall in [
    ((0, 0), (-1, 0), "west"),
    ((0, 0), (0, -1), "north"),
    ((3, 2), (1, 0), "east"),
    ((3, 2), (0, 1), "south"),
]:
    grid[position[0]][position[1]][wall] = False
    assert try_move(grid, position, direction) == position

# Opening a second passage must preserve the first one.
grid = create_grid(height=3, width=4)
remove_wall(grid, (1, 1), (1, 2))
remove_wall(grid, (1, 1), (0, 1))
assert grid[1][1] == {"north": True, "south": False, "east": True, "west": False}
assert try_move(grid, (1, 1), (0, 1)) == (1, 2)
assert try_move(grid, (1, 1), (-1, 0)) == (0, 1)

print("Divider model checks passed!")

from maze import unvisited_neighbors, generate_maze
from copy import deepcopy
from random import Random
from unittest.mock import patch

grid = create_grid(height=3, width=4)
before = deepcopy(grid)
assert set(unvisited_neighbors(grid, (0, 0), {(0, 0)})) == {(1, 0), (0, 1)}
assert set(unvisited_neighbors(grid, (1, 1), {(1, 1), (2, 1)})) == {
    (0, 1), (1, 0), (1, 2)
}
assert unvisited_neighbors(grid, (0, 0), {(0, 0), (1, 0), (0, 1)}) == []
assert grid == before, "Finding neighbors must not change walls"

for width, height in [(4, 3), (3, 5), (1, 1), (1, 4), (4, 1)]:
    for seed in range(5):
        rng = Random(seed)
        with patch("maze.random.choice", side_effect=rng.choice):
            grid = generate_maze(width=width, height=height)
        assert len(grid) == width
        assert all(len(column) == height for column in grid)
        assert all(
            set(cell) == {"north", "south", "east", "west"}
            and all(type(value) is bool for value in cell.values())
            for column in grid for cell in column
        )
        assert all(grid[x][0]["north"] and grid[x][-1]["south"] for x in range(width))
        assert all(grid[0][y]["west"] and grid[-1][y]["east"] for y in range(height))
        for x in range(width):
            for y in range(height):
                if x + 1 < width:
                    assert grid[x][y]["east"] == grid[x + 1][y]["west"]
                if y + 1 < height:
                    assert grid[x][y]["south"] == grid[x][y + 1]["north"]

        reached = {(0, 0)}
        pending = [(0, 0)]
        while pending:
            position = pending.pop()
            for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                neighbor = try_move(grid, position, direction)
                if neighbor not in reached:
                    reached.add(neighbor)
                    pending.append(neighbor)
        assert len(reached) == width * height, "Every cell must be reachable"
        openings = sum(not wall for column in grid for cell in column for wall in cell.values())
        assert openings == 2 * (width * height - 1), "A DFS maze has one connection per new cell"

print("Generation checks passed!")

# Win condition
from maze import has_won

for width, height in [(4, 3), (3, 5), (1, 1)]:
    grid = create_grid(height=height, width=width)
    assert has_won(grid, (width - 1, height - 1)), "Exit follows both grid dimensions"
    if width * height > 1:
        assert not has_won(grid, (0, 0))
        assert not has_won(grid, (width - 1, height)), "Outside the grid is not a win"

print("Win checks passed!")

# Fog uses (x, y) coordinates and includes walls and diagonals
from maze import visible_squares

grid = create_grid(height=3, width=5)
before = deepcopy(grid)
assert visible_squares(grid, (2, 1), radius=1) == {
    (x, y) for x in range(1, 4) for y in range(3)
}
assert visible_squares(grid, (0, 0), radius=1) == {
    (0, 0), (1, 0), (0, 1), (1, 1)
}
assert visible_squares(grid, (4, 2), radius=1) == {
    (3, 1), (4, 1), (3, 2), (4, 2)
}, "Clip at the right and bottom edges of an x-first grid"
assert visible_squares(grid, (2, 1), radius=0) == {(2, 1)}
assert visible_squares(grid, (2, 1), radius=10) == {
    (x, y) for x in range(5) for y in range(3)
}
assert isinstance(visible_squares(grid, (0, 0)), set)
assert grid == before, "Visibility must not modify maze walls"

print("Fog checks passed!")

# BFS contract: return a path including both endpoints, or None if unreachable.
from maze import shortest_path

grid = create_grid(height=2, width=3)
assert shortest_path(grid, (0, 0), (0, 0)) == [(0, 0)]
assert shortest_path(grid, (0, 0), (2, 0)) is None

# Two routes to the same exit: a four-move detour and a two-move shortcut.
for first, second in [
    ((0, 0), (0, 1)), ((0, 1), (1, 1)),
    ((1, 1), (2, 1)), ((2, 1), (2, 0)),
    ((0, 0), (1, 0)), ((1, 0), (2, 0)),
]:
    remove_wall(grid, first, second)
before = deepcopy(grid)
assert shortest_path(grid, (0, 0), (2, 0)) == [(0, 0), (1, 0), (2, 0)]
assert shortest_path(grid, (2, 0), (0, 0)) == [(2, 0), (1, 0), (0, 0)]
assert grid == before, "Pathfinding must preserve the maze"

with patch("maze.random.choice", side_effect=Random(7).choice):
    grid = generate_maze(width=4, height=3)
path = shortest_path(grid, (0, 0), (3, 2))
assert path is not None
assert path[0] == (0, 0) and path[-1] == (3, 2)
assert len(path) == len(set(path)), "A shortest path does not revisit cells"
for first, second in zip(path, path[1:]):
    direction = (second[0] - first[0], second[1] - first[1])
    assert abs(direction[0]) + abs(direction[1]) == 1
    assert try_move(grid, first, direction) == second, "Paths must respect walls"

print("Shortest-path checks passed!")
