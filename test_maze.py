from maze import maze, find_marker, is_walkable, try_move, has_won, generate_maze, unvisited_neighbors
from unittest.mock import patch
from random import Random
from contextlib import redirect_stdout
from io import StringIO

assert find_marker(maze, "S") == (1, 1)
assert find_marker(maze, "E") == (2, 5)
assert is_walkable(maze, 1, 1)
assert not is_walkable(maze, 1, 2)
assert not is_walkable(maze, -1, 1)
assert not is_walkable(maze, 5, 1)
assert not is_walkable(maze, 1, -1)
assert not is_walkable(maze, 1, 7)
assert try_move(maze, (1, 1), (1, 0)) == (2, 1)   # down
assert try_move(maze, (1, 1), (0, 1)) == (1, 1)   # wall
assert try_move(maze, (1, 1), (-1, 0)) == (1, 1)  # wall
assert has_won(maze, (2, 5))
assert not has_won(maze, (1, 1))
assert not has_won(maze, (3, 5))

# Full generation: cover all logical cells and connect every passage.
for height, width in [(5, 7), (9, 13), (13, 9)]:
    for seed in range(5):
        rng = Random(seed)
        # Repeatable randomness; hide the generator's temporary debug printing.
        with patch("maze.random.choice", side_effect=rng.choice), redirect_stdout(StringIO()):
            grid = generate_maze(height=height, width=width)
        assert len(grid) == height
        assert all(len(row) == width for row in grid)
        assert all(square in "#.SE" for row in grid for square in row)
        assert sum(row.count("S") for row in grid) == 1
        assert sum(row.count("E") for row in grid) == 1
        assert find_marker(grid, "S") == (1, 1)
        assert find_marker(grid, "E") == (height - 2, width - 2)
        assert not has_won(grid, (1, 1))
        assert has_won(grid, (height - 2, width - 2))
        assert all(square == "#" for square in grid[0] + grid[-1])
        assert all(row[0] == row[-1] == "#" for row in grid)
        assert all(
            grid[r][c] in ".SE"
            for r in range(1, height - 1, 2)
            for c in range(1, width - 1, 2)
        ), "Backtrack to visit every logical cell"

        passages = {
            (r, c) for r, row in enumerate(grid)
            for c, square in enumerate(row) if square in ".SE"
        }
        # Independently explore the result to verify that no passage is isolated.
        reached = {(1, 1)}
        pending = [(1, 1)]
        while pending:
            r, c = pending.pop()
            for neighbor in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
                if neighbor in passages and neighbor not in reached:
                    reached.add(neighbor)
                    pending.append(neighbor)
        assert (height - 2, width - 2) in reached, "Exit must be reachable"
        assert reached == passages, "Every passage must connect to the start"
        cell_count = ((height - 1) // 2) * ((width - 1) // 2)
        assert len(passages) == 2 * cell_count - 1, "Carve one connection per new cell"

# Mutating one row must not change the others.
grid[2][0] = "."
assert all(grid[r][0] == "#" for r in range(height) if r != 2)

# Neighbors must stay inside the border and exclude visited destinations.
grid = [["#" for _ in range(7)] for _ in range(5)]
grid[1][1] = "."
assert set(unvisited_neighbors(grid, (1, 1))) == {(3, 1), (1, 3)}
grid[3][1] = "."
assert set(unvisited_neighbors(grid, (1, 1))) == {(1, 3)}, "Exclude visited cells"
assert set(unvisited_neighbors(grid, (3, 5))) == {(1, 5), (3, 3)}

print("Movement and generation checks passed!")

# Next milestone: a square of light, clipped at the grid edges.
from maze import visible_squares

fog_grid = [list("#####") for _ in range(5)]
assert visible_squares(fog_grid, (2, 2), radius=1) == {
    (r, c) for r in range(1, 4) for c in range(1, 4)
}, "Include the player, diagonals, and walls"
assert visible_squares(fog_grid, (0, 0), radius=1) == {
    (0, 0), (0, 1), (1, 0), (1, 1)
}, "Clip visibility at the grid edges"
assert visible_squares(fog_grid, (2, 2), radius=0) == {(2, 2)}
assert visible_squares(fog_grid, (2, 2), radius=10) == {
    (r, c) for r in range(5) for c in range(5)
}
assert fog_grid == [list("#####") for _ in range(5)], "Visibility must not change the maze"

print("All checks passed!")
