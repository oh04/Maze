from maze import maze, find_marker, is_walkable, try_move, has_won

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