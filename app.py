import tkinter as tk
from maze import maze, is_walkable, find_marker, try_move, has_won

def draw_maze(canvas, maze, position):
    canvas.delete("all")
    for y, row in enumerate(maze):
        for x, square in enumerate(row):
            xCon = x * 40
            yCon = y * 40
            if not is_walkable(maze, y, x):
                canvas.create_rectangle(xCon, yCon, xCon + 40, yCon + 40, fill="gray")
            elif square == "E":
                canvas.create_rectangle(xCon, yCon, xCon + 40, yCon + 40, fill="green")
            else:
                canvas.create_rectangle(xCon, yCon, xCon + 40, yCon + 40, fill="white")
            if (y, x) == position:
                canvas.create_oval(xCon, yCon, xCon + 40, yCon + 40, fill="blue")

def main():
    window = tk.Tk()
    window.title("Maze")
    canvas = tk.Canvas(window, width=280, height=200)
    canvas.pack()
    position = find_marker(maze, "S")
    status = tk.Label(window, text="Reach green exit")
    status.pack()
    draw_maze(canvas, maze, position)

    def on_key(event):
        nonlocal position
        if has_won(maze, position):
             return
        if event.keysym in ("Down", "s", "S"):
            position = try_move(maze, position, (1, 0))
        elif event.keysym in ("Up", "w", "W"):
            position = try_move(maze, position, (-1, 0))
        elif event.keysym in ("Left", "a", "A"):
                position = try_move(maze, position, (0, -1))
        elif event.keysym in ("Right", "d", "D"):
                position = try_move(maze, position, (0, 1))
        draw_maze(canvas, maze, position)
        if has_won(maze, position):
             status.config(text="You won!")
        print(event.keysym)
    
    window.bind("<KeyPress>", on_key)
    window.mainloop()

if __name__ == "__main__":
    main()