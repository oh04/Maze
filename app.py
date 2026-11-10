import tkinter as tk
from maze import try_move, has_won, generate_maze, visible_squares, shortest_path

def draw_maze(canvas, maze, position, revealed, visible, fog_enabled):
    shortest = shortest_path(maze, (0, 0), (len(maze) - 1, len(maze[0]) - 1))
    won = has_won(maze, position)
    canvas.delete("all")
    for x, _ in enumerate(maze):
        for y, square in enumerate(_):
            xCon = x * 40
            yCon = y * 40
            if fog_enabled and not won:
                canvas.create_rectangle(xCon, yCon, xCon + 40, yCon + 40, fill="gray", outline="")
            else:
                canvas.create_rectangle(xCon, yCon, xCon + 40, yCon + 40, fill="white", outline="")
            if (x, y) in visible:
                canvas.create_rectangle(xCon, yCon, xCon + 40, yCon + 40, fill="white", outline="")
            elif (x, y) in revealed and fog_enabled and not won:
                canvas.create_rectangle(xCon, yCon, xCon + 40, yCon + 40, fill="lightgray", outline="")
            if square["north"] and ((x, y) in revealed or not fog_enabled or won):
                canvas.create_line(xCon, yCon, xCon + 40, yCon, width=2, fill="black")
            if square["south"] and ((x, y) in revealed or not fog_enabled or won):
                canvas.create_line(xCon, yCon + 40, xCon + 40, yCon + 40, width=2, fill="black")
            if square["east"] and ((x, y) in revealed or not fog_enabled or won):
                canvas.create_line(xCon + 40, yCon, xCon + 40, yCon + 40, width=2, fill="black")
            if square["west"] and ((x, y) in revealed or not fog_enabled or won):
                canvas.create_line(xCon, yCon, xCon, yCon + 40, width=2, fill="black")
            if (x, y) in shortest and won:
                canvas.create_oval(xCon + 2, yCon + 2, xCon + 36, yCon + 36, fill="lightgreen")
            if (x == 0 and y == 0  and (x, y) in visible and fog_enabled) or (x == 0 and y == 0 and not fog_enabled):
                canvas.create_rectangle(xCon, yCon, xCon + 40, yCon + 40, fill="yellow", outline="")
            elif x == len(maze) - 1 and y == len(maze[x]) - 1:
                canvas.create_rectangle(xCon + 1, yCon + 1, xCon + 39, yCon + 39, fill="green", outline="")
            if (x, y) == position:
                canvas.create_oval(xCon + 2, yCon + 2, xCon + 36, yCon + 36, fill="blue")

def main():
    window = tk.Tk()
    window.title("Maze")
    width = 13
    height = 9
    move_count = 0
    canvas = tk.Canvas(window, width=width*40, height=height*40)
    canvas.pack()
    status = tk.Label(window, text="Reach green exit")
    status.pack()
    status2 = tk.Label(window, text=f"Move count: {move_count}")
    status2.pack()

    def on_key(event):
        nonlocal position
        nonlocal visible
        nonlocal revealed
        nonlocal move_count
        temp = position
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
        if temp != position:
            move_count += 1
        visible = visible_squares(maze, position, light_radius)
        revealed.update(visible)
        draw_maze(canvas, maze, position, revealed, visible, fog_enabled)
        if has_won(maze, position):
            status.config(text="win")
            status3.config(text=f"Lowest move count: {len(shortest_path(maze, (0, 0), (len(maze) - 1, len(maze[0]) - 1))) - 1}")
        status2.config(text=f"Move count: {move_count}")
        print(event.keysym)

    def new_maze():
        nonlocal position
        nonlocal maze
        nonlocal visible
        nonlocal revealed
        nonlocal move_count
        maze = generate_maze(width, height)
        position = (0, 0)
        move_count = 0
        visible = visible_squares(maze, position, light_radius)
        revealed = visible.copy()
        status.config(text="Reach green exit")
        status2.config(text=f"Move count: {move_count}")
        status3.config(text="")
        draw_maze(canvas, maze, position, revealed, visible, fog_enabled)

    def flip_vis():
        nonlocal fog_enabled
        fog_enabled = not fog_enabled
        draw_maze(canvas, maze, position, revealed, visible, fog_enabled)

    fog_enabled = False
    light_radius = 1
    visible = set()
    revealed = visible.copy()
    maze = generate_maze(width, height)
    position = (0, 0)
    button = tk.Button(window, command=new_maze, text="New Maze")
    button.pack()
    button2 = tk.Button(window, command=flip_vis, text="toggle visibility")
    button2.pack()
    status3 = tk.Label(window, text=f"")
    status3.pack()

    new_maze()

    window.bind("<KeyPress>", on_key)
    window.mainloop()

if __name__ == "__main__":
    main()