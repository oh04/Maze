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