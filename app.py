import tkinter as tk
from tkinter import ttk
from maze import try_move, has_won, generate_maze, visible_squares, shortest_path, light_diag, get_diff

def draw_maze(canvas, maze, position, revealed, visible, fog_enabled, shortest, cell_size, visited, radius, give_up, show_revealed):
    round_over = has_won(maze, position) or give_up
    canvas.delete("all")
    for x, column in enumerate(maze):
        for y, square in enumerate(column):
            strength = light_diag(position, (x, y), radius)
            x_coord = x * cell_size
            y_coord = y * cell_size
            show_walls = (x, y) in visible or not fog_enabled or round_over or (show_revealed and (x, y) in revealed and (x, y) not in visible)
            if not fog_enabled or round_over or ((x, y) in visible and strength == 1):
                canvas.create_rectangle(x_coord, y_coord, x_coord + cell_size, y_coord + cell_size, fill="white", outline="")
            else:
                if strength == 0.5:
                    canvas.create_rectangle(x_coord, y_coord, x_coord + cell_size, y_coord + cell_size, fill="#E8E8E8", outline="")
                elif (x, y) in revealed and show_revealed:
                    canvas.create_rectangle(x_coord, y_coord, x_coord + cell_size, y_coord + cell_size, fill="lightgray", outline="")
                else:
                    canvas.create_rectangle(x_coord, y_coord, x_coord + cell_size, y_coord + cell_size, fill="gray", outline="")
            if x == 0 and y == 0:
                canvas.create_rectangle(x, y, cell_size, cell_size, fill="yellow", outline="")
            elif x == len(maze) - 1 and y == len(maze[x]) - 1:
                canvas.create_rectangle(x_coord + 1, y_coord + 1, x_coord + cell_size - 1, y_coord + cell_size - 1, fill="green", outline="")
            if square["north"] and show_walls:
                canvas.create_line(x_coord, y_coord, x_coord + cell_size, y_coord, width=2, fill="black")
            if square["south"] and show_walls:
                canvas.create_line(x_coord, y_coord + cell_size, x_coord + cell_size, y_coord + cell_size, width=2, fill="black")
            if square["east"] and show_walls:
                canvas.create_line(x_coord + cell_size, y_coord, x_coord + cell_size, y_coord + cell_size, width=2, fill="black")
            if square["west"] and show_walls:
                canvas.create_line(x_coord, y_coord, x_coord, y_coord + cell_size, width=2, fill="black")
    if round_over:
        draw_path(canvas, visited, cell_size, "blue")
        draw_path(canvas, shortest, cell_size, "lightgreen")
    player_x, player_y = position
    player_x *= cell_size
    player_y *= cell_size
    canvas.create_oval(player_x + 2, player_y + 2, player_x + cell_size - 4, player_y + cell_size - 4, fill="blue")

def draw_path(canvas, path, cell_size, color):
    for first, second in zip(path, path[1:]):
        x1, y1 = first
        x2, y2 = second
        x1 = x1 * cell_size + cell_size / 2
        y1 = y1 * cell_size + cell_size / 2
        x2 = x2 * cell_size + cell_size / 2
        y2 = y2 * cell_size + cell_size / 2      
        canvas.create_line(x1, y1, x2, y2, width=6, fill=color)

def main():
    window = tk.Tk()
    window.title("Maze")
    move_count = 0
    cell_size = 40
    give_up = False
    active_config = get_diff("Medium")
    width = active_config["width"]
    height = active_config["height"]
    fog_enabled = active_config["fog_enabled"]
    light_radius = active_config["light_radius"]
    show_revealed = active_config["show_revealed"]
    visible = set()
    revealed = visible.copy()
    maze = None
    position = (0, 0)
    shortest = []
    visited = []
    settings_open = False

    def redraw():
        draw_maze(canvas, maze, position, revealed, visible, fog_enabled, shortest, cell_size, visited, light_radius, give_up, show_revealed)

    def new_maze():
        nonlocal position, maze, visible, revealed, move_count, shortest, visited, give_up
        maze = generate_maze(width, height)
        position = (0, 0)
        move_count = 0
        shortest = shortest_path(maze, position, (len(maze) - 1, len(maze[0]) - 1))
        visible = visible_squares(maze, position, light_radius)
        revealed = visible.copy()
        visited = [position]
        give_up = False
        results_label.config(text="Reach green exit")
        moves_label.config(text=f"Move count: {move_count}")
        lowest_moves.config(text="")
        give_up_button.config(state="normal")
        redraw()

    def on_key(event):
        nonlocal position, visible, revealed, move_count, visited
        if settings_open:
            return
        temp = position
        if has_won(maze, position) or give_up:
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
            visited.append(position)
        visible = visible_squares(maze, position, light_radius)
        revealed.update(visible)
        redraw()
        if has_won(maze, position):
            results_label.config(text="win")
            lowest_moves.config(text=f"Lowest move count: {len(shortest) - 1}")
            give_up_button.config(state="disabled")
        moves_label.config(text=f"Move count: {move_count}")

    def gave_up():
        nonlocal give_up
        if has_won(maze, position) or give_up or settings_open:
            return
        results_label.config(text="gave up")
        lowest_moves.config(text=f"Lowest move count: {len(shortest) - 1}")
        give_up = True
        redraw()
        give_up_button.config(state="disabled")

    def open_settings():

        def set_settings():
            state = "normal" if difficulty.get() == "Custom" else "disabled"
            for control in preset_list:
                control.config(state=state)
            if difficulty.get() == "Custom" and not custom_fog.get():
                revealed_check.config(state="disabled")
                radius_slider.config(state="disabled")

        def update_settings():
            current_difficulty = difficulty.get()
            set_settings()
            if current_difficulty == "Custom":
                return
            current_preset = get_diff(current_difficulty)
            custom_width.set(current_preset["width"])
            custom_height.set(current_preset["height"])
            custom_radius.set(current_preset["light_radius"])
            custom_fog.set(current_preset["fog_enabled"])
            custom_revealed.set(current_preset["show_revealed"])

        def cancel():
            nonlocal settings_open
            settings_open = False
            settings_panel.destroy()
            new_maze_button.config(state="normal")
        
        def set_apply():
            nonlocal fog_enabled, light_radius, visible, revealed, active_config, width, height, show_revealed, cell_size, settings_open
            custom = {
                "width": custom_width.get(),
                "height": custom_height.get(),
                "light_radius": custom_radius.get(),
                "fog_enabled": custom_fog.get(),
                "show_revealed": custom_revealed.get()
            }
            active_config = get_diff(difficulty.get(), custom)
            fog_enabled = active_config["fog_enabled"]
            light_radius = active_config["light_radius"]
            width = active_config["width"]
            height = active_config["height"]
            show_revealed = active_config["show_revealed"]
            cell_size = min(40, 720 // width, 480 // height)
            canvas.config(width=width * cell_size, height=height * cell_size)
            new_maze()
            cancel()

        nonlocal settings_open
        if settings_open:
            return
        settings_panel = tk.Frame(window)
        settings_panel.place(relx=0.5, rely=0.5, anchor="center")
        settings_panel.lift()
        settings_open = True
        new_maze_button.config(state="disabled")
        difficulty = tk.StringVar(value=active_config["difficulty"])
        custom_width = tk.IntVar(value=active_config["width"])
        custom_height = tk.IntVar(value=active_config["height"])
        custom_radius = tk.IntVar(value=active_config["light_radius"])
        custom_fog = tk.BooleanVar(value=active_config["fog_enabled"])
        custom_revealed = tk.BooleanVar(value=active_config["show_revealed"])
        notebook = ttk.Notebook(settings_panel)
        notebook.pack(fill="both", expand=True)
        difficulty_tab = ttk.Frame(notebook)
        stats_tab = ttk.Frame(notebook)
        notebook.add(difficulty_tab, text="Difficulty")
        notebook.add(stats_tab, text="Stats")
        choices = ttk.Frame(difficulty_tab)
        choices.pack(side="left")
        settings = ttk.Frame(difficulty_tab)
        settings.pack(side="right")
        ttk.Label(settings, text="Enable Fog").grid(row=0, column=0, sticky="w")
        fog_check = tk.Checkbutton(settings, variable=custom_fog, command=set_settings)
        fog_check.grid(row=0, column=1)
        ttk.Label(settings, text="Show Explored Cells").grid(row=1, column=0, sticky="w")
        revealed_check = tk.Checkbutton(settings, variable=custom_revealed)
        revealed_check.grid(row=1, column=1)
        ttk.Label(settings, text="Radius View").grid(row=2, column=0, sticky="w")
        radius_slider = tk.Scale(settings, from_=1, to=5, orient="horizontal", resolution=1, variable=custom_radius, length=180,)
        radius_slider.grid(row=2, column=1)
        ttk.Label(settings, text="Width").grid(row=3, column=0, sticky="w")
        width_slider = tk.Scale(settings, from_=4, to=30, orient="horizontal", resolution=1, variable=custom_width, length=180,)
        width_slider.grid(row=3, column=1)
        ttk.Label(settings, text="Height").grid(row=4, column=0, sticky="w")
        height_slider = tk.Scale(settings, from_=4, to=30, orient="horizontal", resolution=1, variable=custom_height, length=180,)
        height_slider.grid(row=4, column=1)
        preset_list = [fog_check, revealed_check, radius_slider, width_slider, height_slider]
        set_settings()
        ttk.Radiobutton(choices, text="Easy", variable=difficulty, value="Easy", command=update_settings, padding=12).pack(anchor="w")
        ttk.Radiobutton(choices, text="Medium", variable=difficulty, value="Medium", command=update_settings, padding=12).pack(anchor="w")
        ttk.Radiobutton(choices, text="Hard", variable=difficulty, value="Hard", command=update_settings, padding=12).pack(anchor="w")
        ttk.Radiobutton(choices, text="Impossible", variable=difficulty, value="Impossible", command=update_settings, padding=12).pack(anchor="w")
        ttk.Radiobutton(choices, text="Custom", variable=difficulty, value="Custom", command=update_settings, padding=12).pack(anchor="w")
        apply_button = tk.Button(settings_panel,command=set_apply, text="Apply")
        apply_button.pack(side="right")
        cancel_button = tk.Button(settings_panel, command=cancel, text="Cancel")
        cancel_button.pack(side="right")

    toolbar = tk.Frame(window)
    toolbar.pack(side="top", fill="x")     
    settings_button=tk.Button(toolbar, command=open_settings, text="Settings")
    settings_button.pack(side="right")
    canvas = tk.Canvas(window, width=width*cell_size, height=height*cell_size)
    canvas.pack()
    results_label = tk.Label(window, text="Reach green exit")
    results_label.pack()
    moves_label = tk.Label(window, text=f"Move count: {move_count}")
    moves_label.pack()
    new_maze_button = tk.Button(window, command=new_maze, text="New Maze")
    new_maze_button.pack()
    give_up_button = tk.Button(window, command=gave_up, text="Give up")
    give_up_button.pack()
    lowest_moves = tk.Label(window, text="")
    lowest_moves.pack()

    new_maze()
    window.bind("<KeyPress>", on_key)
    window.mainloop()

if __name__ == "__main__":
    main()