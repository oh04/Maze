import tkinter as tk
from maze import maze, try_move, has_won, generate_maze

def draw_maze(canvas, maze, position):
    canvas.delete("all")
    for x, row in enumerate(maze):
        for y, square in enumerate(row):
            xCon = x * 40
            yCon = y * 40
            canvas.create_rectangle(xCon, yCon, xCon + 40, yCon + 40, fill="white")
            if x == 0 and y == 0:
                canvas.create_rectangle(xCon, yCon, xCon + 40, yCon + 40, fill="gray")
            elif x == len(maze) - 1 and y == len(maze[x]) - 1:
                canvas.create_rectangle(xCon, yCon, xCon + 40, yCon + 40, fill="green")
            if (x, y) == position:
                canvas.create_oval(xCon, yCon, xCon + 40, yCon + 40, fill="blue")
            if square["north"]:
                canvas.create_line(xCon, yCon, xCon + 40, yCon, width=2, fill="black")
            if square["south"]:
                canvas.create_line(xCon, yCon + 40, xCon + 40, yCon + 40, width=2, fill="black")
            if square["east"]:
                canvas.create_line(xCon + 40, yCon, xCon + 40, yCon + 40, width=2, fill="black")
            if square["west"]:
                canvas.create_line(xCon, yCon, xCon, yCon + 40, width=2, fill="black")

def main():
    window = tk.Tk()
    window.title("Maze")
    width = 13
    height = 9
    canvas = tk.Canvas(window, width=width*40, height=height*40)
    canvas.pack()
    status = tk.Label(window, text="Reach green exit")
    status.pack()

    def on_key(event):
        nonlocal position
        if has_won(maze, position):
             return
        if event.keysym in ("Up", "w", "W"):
            position = try_move(maze, position, (0, -1))
        elif event.keysym in ("Left", "a", "A"):
            position = try_move(maze, position, (-1, 0))
        elif event.keysym in ("Down", "s", "S"):
            position = try_move(maze, position, (0, 1))
        elif event.keysym in ("Right", "d", "D"):
            position = try_move(maze, position, (1, 0))
        draw_maze(canvas, maze, position)
        if has_won(maze, position):
             status.config(text="win")
        print(event.keysym)

    def new_maze():
         nonlocal position
         nonlocal maze
         maze = generate_maze(width, height)
         position = (0, 0)
         status.config(text="Reach green exit")
         draw_maze(canvas, maze, position)

    maze = generate_maze(width, height)
    position = (0, 0)
    button = tk.Button(window, command=new_maze, text="New Maze")
    button.pack()

    new_maze()

    window.bind("<KeyPress>", on_key)
    window.mainloop()

if __name__ == "__main__":
    main()