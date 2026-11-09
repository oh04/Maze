import random

def main():
    print()

maze = ["#######", "#S#...#", "#.#.#E#", "#...#.#", "#######",]

def find_marker(maze, marker):
    for row_index, row in enumerate(maze):
        for column_index, square in enumerate(row):
            if square == marker:
                return (row_index, column_index)
    return 0

def is_walkable(maze, row, column):
    if 0 <= row <= len(maze) - 1 and 0 <= column <= len(maze[row]) - 1:
        return maze[row][column] in ".SE"
    return False

def try_move(maze, position, direction):
    row, column = position
    dirR, dirC = direction
    if(is_walkable(maze, row + dirR, column + dirC)):
        return (row + dirR, column + dirC)
    return position

def has_won(maze, position):
    return position == find_marker(maze, "E")

def generate_maze(width, height):
    grid = [["#" for _ in range(width)] for _ in range(height)]
    stack = [(1, 1)]
    grid[1][1] = "."
    while stack:
        row, col = stack[-1]
        neighbors = unvisited_neighbors(grid, stack[-1])
        if not neighbors:
            stack.pop()
            continue
        new_row, new_col = random.choice(neighbors)
        mid_row = (row + new_row) // 2
        mid_col = (col + new_col) // 2
        grid[new_row][new_col] = "."
        grid[mid_row][mid_col] = "."
        stack.append((new_row, new_col))
    for row in grid:
        print("".join(row))
    grid[1][1] = "S"
    grid[height - 2][width - 2] = "E"
    return grid

def unvisited_neighbors(grid, position):
    row, column = position
    neighbors = []
    for row_change, column_change in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        new_row = row + row_change
        new_col = column + column_change
        if 0 < new_row < len(grid) - 1 and 0 < new_col < len(grid[0]) - 1 and grid[new_row][new_col] == "#":
            neighbors.append((new_row, new_col))
    return neighbors