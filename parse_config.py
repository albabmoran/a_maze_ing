import sys
from typing import Optional


class InvalidValue(Exception):
    """
    Exception raised when a configuration key has
    an invalid value format or range.
    """
    pass


class Config:
    """
    Handles loading, parsing, and verifying maze configuration files.

    Attributes:
        width (int): The width of the maze.
        height (int): The height of the maze.
        entry (tuple[int, int]): Coordinates (x, y) for the maze entrance.
        exit (tuple[int, int]): Coordinates (x, y) for the maze exit.
        output_file (str): The name of the file where the output will be saved.
        perfect (bool): True if the maze is perfect, False otherwise.
        seed (Optional[int]): The random generation seed. Defaults to None.
    """

    def __init__(self) -> None:
        """
        Initializes an empty Config instance with uninitialized parameters.
        """
        self.width: int
        self.height: int
        self.entry: tuple[int, int]
        self.exit: tuple[int, int]
        self.output_file: str
        self.perfect: bool
        self.seed: Optional[int] = None

    def read_and_validate_format(self) -> list[str]:
        """
        Reads configuration data from a file and validates syntax and
        constraints.

        Verifies that command line arguments are correct, attempts
        to open the configuration file, validates line formatting
        (KEY=VALUE with no spaces), and safely parses each valid parameter
        according to its type.

        Returns:
            list[str]: list containing all the valid keys successfully parsed.
        """
        if len(sys.argv) != 2:
            print("ERROR: invalid number of arguments. "
                  "<Usage: python3 a_maze_ing.py config.txt>", file=sys.stderr)
            sys.exit(2)

        try:
            with open("config.txt", "r") as file:
                info = file.read()
        except OSError as e:
            print(f"ERROR reading file: {e}", file=sys.stderr)
            sys.exit(e.errno)

        valid_keys = [
            "WIDTH", "HEIGHT", "ENTRY", "EXIT",
            "OUTPUT_FILE", "PERFECT", "SEED"
        ]
        keys: list[str] = []
        content = info.split('\n')
        for line in content:
            if not line.strip() or line.startswith("#"):
                continue
            index = line.find("=")
            if (
                index < 0
                or index != line.rfind("=")
                or " " in line
                or not line[:index]
                or not line[index + 1:]
            ):
                print("ERROR: config.txt should have lines "
                      "with KEY=VALUE and no spaces", file=sys.stderr)
                sys.exit(1)

            k, v = line.split("=")
            if k not in valid_keys:
                print(f"ERROR: invalid parameter {k}", file=sys.stderr)
                sys.exit(1)
            if k in keys:
                print(f"ERROR: duplicated key {k}", file=sys.stderr)
                sys.exit(1)

            if k == "WIDTH" or k == "HEIGHT":
                try:
                    value = int(v)
                    if value <= 0:
                        raise InvalidValue(f"{v} is an invalid value for {k}")
                    if k == "WIDTH":
                        self.width = value
                    if k == "HEIGHT":
                        self.height = value
                    keys.append(k)
                except ValueError:
                    print(f"ERROR: {k} must be an int: <{v}>", file=sys.stderr)
                    sys.exit(1)
                except InvalidValue as e:
                    print(f"ERROR: {e}", file=sys.stderr)
                    sys.exit(1)

            elif k == "ENTRY" or k == "EXIT":
                try:
                    v1, v2 = v.split(",")
                    x = int(v1)
                    y = int(v2)
                    if x < 0 or y < 0:
                        raise InvalidValue(f"both coordinates ({x},{y})"
                                           " must be positive")
                    coord = (x, y)
                    if k == "ENTRY":
                        self.entry = coord
                    if k == "EXIT":
                        self.exit = coord
                    keys.append(k)
                except ValueError:
                    print(f"ERROR: {k} must be an int: <{v}>", file=sys.stderr)
                    sys.exit(1)
                except InvalidValue as e:
                    print(f"ERROR: {e}", file=sys.stderr)
                    sys.exit(1)

            elif k == "OUTPUT_FILE":
                try:
                    if not v.endswith(".txt"):
                        raise InvalidValue("output file must be "
                                           "of format '.txt'")
                    self.output_file = v
                    keys.append(k)
                except InvalidValue as e:
                    print(f"ERROR: {e}", file=sys.stderr)
                    sys.exit(1)

            elif k == "PERFECT":
                try:
                    if v == "True":
                        value = True
                    elif v == "False":
                        value = False
                    else:
                        raise InvalidValue("perfect must be "
                                           "'True' or 'False'")
                    self.perfect = value
                    keys.append(k)
                except InvalidValue as e:
                    print(f"ERROR: {e}", file=sys.stderr)
                    sys.exit(1)

            elif k == "SEED":
                try:
                    value = int(v)
                    self.seed = value
                    keys.append(k)
                except ValueError:
                    print("ERROR: seed must be of type "
                          "int", file=sys.stderr)
                    sys.exit(1)

        if self.height == 1 and self.width == 1:
            print("ERROR: invalid values, cannot "
                  "generate an 1x1 maze", file=sys.stderr)
            sys.exit(1)
        return keys

    def check_mandatory_keys(self, keys: list[str]) -> None:
        """
        Validates that all mandatory configuration parameters are present.

        Compares the list of parsed keys against the predefined list of
        mandatory keys.
        Prints missing values and aborts execution if any mandatory key is
        missing.

        Args:
            keys (list[str]): list of all unique keys found during file
            processing.
        """
        mandatory_keys = [
            "WIDTH", "HEIGHT", "ENTRY", "EXIT",
            "OUTPUT_FILE", "PERFECT"
        ]
        dif = set(mandatory_keys) - set(keys)
        if dif:
            missing = ", ".join(sorted(dif))
            print("ERROR: not all keys present. "
                  f"Missing: {missing}", file=sys.stderr)
            sys.exit(1)

    def check_entry_and_exit(self) -> None:
        """
        Ensures entry and exit logical constraints are respected.

        Verifies that the entrance and exit are located at completely different
        points, and checks that both sets of coordinates fit inside the defined
        bounds of the maze (width and height).
        """
        if self.entry == self.exit:
            print("ERROR: entry and exit must be different", file=sys.stderr)
            sys.exit(1)
        coord = [self.entry, self.exit]
        for c in coord:
            x, y = c[0], c[1]
            if x >= self.width or y >= self.height:
                print(f"ERROR: {c} is outside the maze", file=sys.stderr)
                sys.exit(1)


config = Config()
keys = config.read_and_validate_format()
config.check_mandatory_keys(keys)
config.check_entry_and_exit()
