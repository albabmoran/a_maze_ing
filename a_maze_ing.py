from parse_config import Config
from mazegen import MazeGen
from mazedraw import ProgramState, MazeDrawer
from menu import Menu


def main() -> None:
    config = Config()
    keys = config.read_and_validate_format()
    config.check_mandatory_keys(keys)
    config.check_entry_and_exit()

    maze = MazeGen(config.width, config.height, config.entry,
                   config.exit, config.output_file,
                   config.perfect, config.seed)
    maze.gen_maze()
    maze.solve_maze()

    state = ProgramState(maze)
    visual = MazeDrawer(state)

    menu = Menu(state, visual)

    visual.mlx.mlx_key_hook(visual.window, menu.key_press, visual)

    visual.mlx.mlx_expose_hook(visual.window, visual.update_screen, state)
    visual.mlx.mlx_loop_hook(visual.mlx_ptr, visual.update_screen, state)

    visual.update_screen(state)

    visual.mlx.mlx_loop(visual.mlx_ptr)

    visual.mlx.mlx_destroy_image(visual.mlx_ptr, visual.img)
    visual.mlx.mlx_destroy_window(visual.mlx_ptr, visual.window)
    visual.mlx.mlx_release(visual.mlx_ptr)


if __name__ == '__main__':
    main()
