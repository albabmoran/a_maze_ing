from parse_config import Config
from mazegen.mazegen import MazeGen


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


if __name__ == '__main__':
    main()
