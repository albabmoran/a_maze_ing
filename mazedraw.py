from mlx import Mlx
from mazegen import MazeGen


class ProgramState:
    """
    Manages the shared visual layout configurations and state
    for the maze user interfaze.
    """

    def __init__(self, maze: MazeGen) -> None:
        """
        Initializes the shared program state from a core MazeGen instance.

        Args:
            maze (MazeGen): The core maze generation engine instance.
        """

        self.cell_size: int = 30
        self.wall_thick: int = 3

        self.maze_data: MazeGen = maze

        self.show_solution: bool = False

        self.animate_solution: bool = False
        self.current_step: int = 0

        self.current_palette: int = 0
        self.palettes: list[tuple[int, int, int, int, int, int]] = [
            (0x1E293B, 0xF8FAFC, 0x0EA5E9, 0xF97316, 0x10B981, 0xEF4444),
            (0x7F00FF, 0x0D0221, 0x39FF14, 0xFF007F, 0xFFE600, 0x00F0FF),
            (0x2B1E17, 0xF4EAE1, 0xD64045, 0x6E44FF, 0x7A9B76, 0x467194)
        ]
        self.wall_colors: list[int] = [0xC5A059, 0x14342B, 0xE2E8F0,
                                       0x5C0614, 0x2C3E50]
        self.current_wall_color_idx: int = 0

        self.is_running: bool = True
        self.need_redraw: bool = True
        self.need_menu: bool = True

    def reset_visual_state(self) -> None:
        """
        Resets the visual state variables related to solution
        rendering and animation.
        """

        self.show_solution = False
        self.animate_solution = False
        self.current_step = 0

    def regenerate(self) -> None:
        """
        Triggers the generation and solving of a new maze,
        resetting the visual state.
        """

        self.maze_data.gen_maze()
        self.maze_data.solve_maze()
        self.reset_visual_state()
        self.need_redraw = True

    def toggle_solution(self) -> None:
        """
        Toggles the visibility of the complete maze solution and
        disables animation if active.
        """

        self.show_solution = not self.show_solution
        if self.show_solution:
            self.animate_solution = False
        self.need_redraw = True

    def rotate_palette(self) -> None:
        """
        Cycles through the available color palettes sequentially.
        """

        self.current_palette = (self.current_palette + 1) % len(self.palettes)
        self.need_redraw = True

    def rotate_wall_color(self) -> None:
        """
        Cycles through the pre-defined wall colors independently and updates
        the active palette tuple in place.
        """

        self.current_wall_color_idx = ((self.current_wall_color_idx + 1)
                                       % len(self.wall_colors))
        next_color = self.wall_colors[self.current_wall_color_idx]
        palette_list = list(self.palettes[self.current_palette])
        palette_list[0] = next_color
        self.palettes[self.current_palette] = (
            palette_list[0], palette_list[1], palette_list[2],
            palette_list[3], palette_list[4], palette_list[5]
        )

        self.need_redraw = True

    def quit(self) -> None:
        """
        Flags the program state to stop running.
        """

        self.is_running = False

    def toggle_animation(self) -> None:
        """
        Toggles the pathfinding animation state, resetting steps
        and disabling the static solution.
        """

        self.animate_solution = not self.animate_solution
        if self.animate_solution:
            self.show_solution = False
            self.current_step = 0
        self.need_redraw = True

    def advance_animation(self) -> None:
        """
        Advances the maze solution animation by one step until
        the complete path is shown.
        """

        if not self.animate_solution:
            return
        if self.current_step < len(self.maze_data.solution_path) - 1:
            self.current_step += 1
            self.need_redraw = True
        else:
            self.animate_solution = False
            self.show_solution = True
            self.need_redraw = True


class MazeDrawer:
    """
    Handles the canvas view window, graphics context, and pixel buffering.
    """

    def __init__(self, state: ProgramState) -> None:
        """
        Initializes the window and creates the raw pixel image buffer.

        Args:
            state (ProgramState): The shared graphical interface state.
        """

        self.state: ProgramState = state
        self.menu_width: int = 500
        self.menu_height: int = 150

        self.width = max(
            state.maze_data.width * state.cell_size,
            self.menu_width
        )
        self.height: int = ((state.maze_data.height * state.cell_size)
                            + self.menu_height)

        self.mlx: Mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.window = self.mlx.mlx_new_window(
            self.mlx_ptr, self.width, self.height, "A-Maze-Ing - VISUAL"
        )
        self.img = self.mlx.mlx_new_image(self.mlx_ptr, self.width,
                                          self.height)
        img_info = self.mlx.mlx_get_data_addr(self.img)
        self.img_buffer = img_info[0]
        self.size_line = img_info[2]

        self.closed: bool = False

    def draw_square(self, x1: int, y1: int, x2: int,
                    y2: int, color: int) -> None:
        """
        Carves a solid colored square tile directly onto the image data buffer.

        Args:
            x1 (int): Starting pixel coordinate on the X axis.
            y1 (int): Starting pixel coordinate on the Y axis.
            x2 (int): Ending pixel coordinate on the X axis.
            y2 (int): Ending pixel coordinate on the Y axis.
            color (int): Hexadecimal color representation bit mask.
        """

        b = color & 0xFF
        g = (color >> 8) & 0xFF
        r = (color >> 16) & 0xFF

        for y in range(max(0, y1), min(self.height, y2)):
            for x in range(max(0, x1), min(self.width, x2)):
                idx = (y * self.size_line) + (x * 4)
                self.img_buffer[idx] = b
                self.img_buffer[idx + 1] = g
                self.img_buffer[idx + 2] = r
                self.img_buffer[idx + 3] = 255

    def update_screen(self, state: ProgramState) -> None:
        """
        Scans raw cell attributes and writes aligned fine walls to the canvas.

        Draws background tiles, processes static or animated solution overlays
        and stamps fine bounding lines onto the pixel buffer before updating
        the window interface.

        Args:
            state (ProgramState): The shared graphical interface state.
        """

        if not state.need_redraw:
            return
        state.need_redraw = False
        if state.animate_solution:
            state.advance_animation()

        (c_wall, c_path, c_solution,
         c_42, c_entry, c_exit) = state.palettes[state.current_palette]
        size = state.cell_size
        t = state.wall_thick

        for (x, y), cell in state.maze_data.maze.items():
            x_pix = x * size
            y_pix = y * size

            if (x, y) == state.maze_data.entry:
                color = c_entry
            elif (x, y) == state.maze_data.exit:
                color = c_exit
            elif cell.freeze:
                color = c_42
            else:
                color = c_path
            self.draw_square(x_pix, y_pix, x_pix + size, y_pix + size, color)

        if state.show_solution or state.animate_solution:
            if state.animate_solution:
                steps = state.maze_data.solution_path[:state.current_step]
            else:
                steps = state.maze_data.solution_path
            for (x, y) in steps:
                if (
                    (x, y) != state.maze_data.entry
                    and (x, y) != state.maze_data.exit
                ):
                    cx = x * size + (size // 2)
                    cy = y * size + (size // 2)
                    self.draw_square(cx - 6, cy - 6, cx + 6, cy + 6,
                                     c_solution)

        for (x, y), cell in state.maze_data.maze.items():
            x_pix = x * size
            y_pix = y * size
            if cell.walls['north'] == 1:
                self.draw_square(x_pix, y_pix, x_pix + size, y_pix + t, c_wall)
            if cell.walls['east'] == 1:
                self.draw_square(x_pix + size - t, y_pix, x_pix + size,
                                 y_pix + size, c_wall)
            if cell.walls['south'] == 1:
                self.draw_square(x_pix, y_pix + size - t, x_pix + size,
                                 y_pix + size, c_wall)
            if cell.walls['west'] == 1:
                self.draw_square(x_pix, y_pix, x_pix + t, y_pix + size, c_wall)

        if state.need_menu:
            self.draw_menu(state)
            state.need_menu = False
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.window,
                                         self.img, 0, 0)
        self.mlx.mlx_do_sync(self.mlx_ptr)

        return

    def draw_menu(self, state: ProgramState) -> None:
        """
        Calculates the menu position based on the current maze
        dimensions and renders the available keyboard controls
        directly onto the window.

        Args:
            state (ProgramState): Shared program state containing
                                the maze dimensions and visual
                                configuration required to calculate
                                the menu position.
        """

        y = state.maze_data.height * state.cell_size + 40

        self.mlx.mlx_string_put(self.mlx_ptr, self.window, 10,
                                y, 0xFFFFFF, "1-Regenerate maze")
        self.mlx.mlx_string_put(self.mlx_ptr, self.window, 250,
                                y, 0xFFFFFF, "2-Show/Hide solution")
        self.mlx.mlx_string_put(self.mlx_ptr, self.window, 10,
                                y + 25, 0xFFFFFF, "3-Rotate colors")
        self.mlx.mlx_string_put(self.mlx_ptr, self.window, 250,
                                y + 25, 0xFFFFFF, "4-Change wall colors")
        self.mlx.mlx_string_put(self.mlx_ptr, self.window, 10,
                                y + 50, 0xFFFFFF, "5-Animate solution")
        self.mlx.mlx_string_put(self.mlx_ptr, self.window, 250,
                                y + 50, 0xFFFFFF, "6-Quit")

    def close(self) -> None:
        """
        Closes the display window and terminates the main
        graphics rendering loop.
        """

        if self.closed:
            return

        self.closed = True
        self.mlx.mlx_loop_exit(self.mlx_ptr)
