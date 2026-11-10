import tkinter as tk
from maze import try_move, has_won, generate_maze, visible_squares

def draw_maze(canvas, maze, position, revealed, fog_enabled):
    canvas.delete("all")
    for x, row in enumerate(maze):
        for y, square in enumerate(row):
            xCon = x * 40
            yCon = y * 40
            canvas.create_rectangle(xCon, yCon, xCon + 40, yCon + 40, fill="grey", outline="")
            if (x, y) in revealed and fog_enabled:
                canvas.create_rectangle(xCon, yCon, xCon + 40, yCon + 40, fill="white", outline="")
            if square["north"] and (x, y) in revealed:
                canvas.create_line(xCon, yCon, xCon + 40, yCon, width=2, fill="black")
            if square["south"] and (x, y) in revealed:
                canvas.create_line(xCon, yCon + 40, xCon + 40, yCon + 40, width=2, fill="black")
            if square["east"] and (x, y) in revealed:
                canvas.create_line(xCon + 40, yCon, xCon + 40, yCon + 40, width=2, fill="black")
            if square["west"] and (x, y) in revealed:
                canvas.create_line(xCon, yCon, xCon, yCon + 40, width=2, fill="black")
            if x == 0 and y == 0:
                canvas.create_rectangle(xCon, yCon, xCon + 40, yCon + 40, fill="yellow", outline="")
            elif x == len(maze) - 1 and y == len(maze[x]) - 1:
                canvas.create_rectangle(xCon, yCon, xCon + 40, yCon + 40, fill="green", outline="")
            if (x, y) == position:
                canvas.create_oval(xCon, yCon, xCon + 40, yCon + 40, fill="blue")

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
        nonlocal visible
        nonlocal revealed
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
        visible = visible_squares(maze, position, light_radius)
        revealed.update(visible)
        draw_maze(canvas, maze, position, revealed, fog_enabled)
        if has_won(maze, position):
             status.config(text="win")
        print(event.keysym)

    def new_maze():
        nonlocal position
        nonlocal maze
        nonlocal visible
        nonlocal revealed
        maze = generate_maze(width, height)
        position = (0, 0)
        visible = visible_squares(maze, position, light_radius)
        revealed = visible.copy()
        status.config(text="Reach green exit")
        draw_maze(canvas, maze, position, revealed, fog_enabled)

    fog_enabled = True
    light_radius = 1
    visible = set()
    revealed = visible.copy()
    maze = generate_maze(width, height)
    position = (0, 0)
    button = tk.Button(window, command=new_maze, text="New Maze")
    button.pack()

    new_maze()

    window.bind("<KeyPress>", on_key)
    window.mainloop()

if __name__ == "__main__":
    main()