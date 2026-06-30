import random
import sys
from typing import Optional
from collections import deque


class Cell:
    """
    Represents a single cell in the maze with its boundaries and state.
    """

    def __init__(self) -> None:
        """
        Initializes a cell with all four walls closed and reset states.
        """

        self.walls: dict[str, int] = {
            'north': 1,
            'east': 1,
            'south': 1,
            'west': 1
        }
        self.visited: bool = False
        self.freeze: bool = False
        self.hex: str = 'F'


class MazeGen:
    """
    Handles the creation, carving, and formatting of a maze grid.
    """

    def __init__(self, width: int, height: int,
                 entry: tuple[int, int], exit: tuple[int, int],
                 output_file: str, perfect: bool,
                 seed: Optional[int]) -> None:
        """
        Initializes the maze generator with configuration properties.

        Args:
            width (int): The total number of columns in the maze.
            height (int): The total number of rows in the maze.
            entry (tuple[int, int]): Coordinates (x, y) of the maze entrance.
            exit (tuple[int, int]): Coordinates (x, y) of the maze exit.
            perfect (bool): True if the maze has only one unique solution.
            seed (Optional[int]): Random seed value for reproducibility.
        """

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed
        self.maze:  dict[tuple[int, int], Cell] = {}
        self.center: tuple[int, int]
        self.solution_path: list[tuple[int, int]] = []
        self.solution_str: str = ""

    def gen_base(self) -> None:
        """
        Creates the maze dictionary with default closed Cell instances.
        """

        for y in range(self.height):
            for x in range(self.width):
                self.maze[(x, y)] = Cell()

    def calc_center(self) -> list[tuple[int, int]]:
        """
        Calculates candidate center coordinates for the maze.

        Returns:
            list[tuple[int, int]]: A prioritized list of central grid
            positions.
        """

        if self.width % 2 == 0:
            middle_col = (self.width // 2) - 1
        else:
            middle_col = self.width // 2
        if self.height % 2 == 0:
            middle_row = (self.height // 2) - 1
        else:
            middle_row = self.height // 2
        return [(middle_col, middle_row),
                (middle_col, middle_row - 1),
                (middle_col, middle_row + 1),
                (middle_col - 1, middle_row),
                (middle_col + 1, middle_row),
                (middle_col + 1, middle_row + 1),
                (middle_col + 1, middle_row - 1),
                (middle_col - 1, middle_row - 1),
                (middle_col - 1, middle_row + 1)]

    def draw_fortytwo(self) -> None:
        """
        Finds a valid center and freezes cells to form the '42' pattern.
        """

        pos_center = self.calc_center()
        frozen: list[tuple[int, int]] = []
        found_valid: bool = False
        for coord in pos_center:
            frozen = [(coord[0] - 3, coord[1] - 2),
                      (coord[0] - 3, coord[1] - 1),
                      (coord[0] - 3, coord[1]),
                      (coord[0] - 2, coord[1]),
                      (coord[0] - 1, coord[1]),
                      (coord[0] - 1, coord[1] + 1),
                      (coord[0] - 1, coord[1] + 2),
                      (coord[0] + 1, coord[1] - 2),
                      (coord[0] + 2, coord[1] - 2),
                      (coord[0] + 3, coord[1] - 2),
                      (coord[0] + 3, coord[1] - 1),
                      (coord[0] + 3, coord[1]),
                      (coord[0] + 2, coord[1]),
                      (coord[0] + 1, coord[1]),
                      (coord[0] + 1, coord[1] + 1),
                      (coord[0] + 1, coord[1] + 2),
                      (coord[0] + 2, coord[1] + 2),
                      (coord[0] + 3, coord[1] + 2)]
            if self.entry not in frozen and self.exit not in frozen:
                self.center = coord
                found_valid = True
                break
        if found_valid:
            for cell in frozen:
                self.maze[cell].freeze = True
                self.maze[cell].visited = True
        else:
            print("ERROR: couldn't find a position for '42' in which "
                  "entry/exit wasn't blocked. Generating without 42.",
                  file=sys.stderr)
            self.fortytwo = False

    def gen_maze(self) -> None:
        """
        Carves paths through the grid using iterative depth-first search.
        """

        random.seed(self.seed)
        self.gen_base()
        if self.width >= 12 and self.height >= 10:
            self.draw_fortytwo()
        else:
            print("ERROR: maze isn't big enough to draw 42",
                  file=sys.stderr)
            self.fortytwo = False

        origin: tuple[int, int] = self.entry
        self.maze[origin].visited = True
        stack: list[tuple[int, int]] = [origin]

        while stack:
            cell = stack[-1]
            col, row = cell
            valid_ngb: list[tuple[str, str, tuple[int, int]]] = []

            n_col, n_row = col, row - 1
            if 0 <= n_col < self.width and (0 <= n_row < self.height):
                if (
                    not self.maze[(n_col, n_row)].freeze
                    and not self.maze[(n_col, n_row)].visited
                ):
                    valid_ngb.append(('north', 'south', (n_col, n_row)))

            e_col, e_row = col + 1, row
            if 0 <= e_col < self.width and (0 <= e_row < self.height):
                if (
                    not self.maze[(e_col, e_row)].freeze
                    and not self.maze[(e_col, e_row)].visited
                ):
                    valid_ngb.append(('east', 'west', (e_col, e_row)))

            s_col, s_row = col, row + 1
            if 0 <= s_col < self.width and (0 <= s_row < self.height):
                if (
                    not self.maze[(s_col, s_row)].freeze
                    and not self.maze[(s_col, s_row)].visited
                ):
                    valid_ngb.append(('south', 'north', (s_col, s_row)))

            w_col, w_row = col - 1, row
            if 0 <= w_col < self.width and (0 <= w_row < self.height):
                if (
                    not self.maze[(w_col, w_row)].freeze
                    and not self.maze[(w_col, w_row)].visited
                ):
                    valid_ngb.append(('west', 'east', (w_col, w_row)))

            if not valid_ngb:
                stack.pop()
            else:
                dir_act, dir_ngb, next_cell = random.choice(valid_ngb)
                self.maze[cell].walls[dir_act] = 0
                self.maze[next_cell].walls[dir_ngb] = 0
                self.maze[next_cell].visited = True
                stack.append(next_cell)

    def reset_visited(self) -> None:
        """
        Resets the visited status of all non-frozen cells in the maze.
        """

        for i in self.maze.values():
            if not i.freeze:
                i.visited = False

    def bfs(self) -> tuple[list[tuple[int, int]], str]:
        """
        Finds the shortest path from entry to exit using Breadth-First Search.

        This algorithm explores the maze layer by layer using a double-ended
        queue (deque) to guarantee finding the shortest path. It validates
        grid boundaries, wall openings, and visitation records.

        Returns:
            tuple[list[tuple[int, int]], str]: A tuple containing:
                - list[tuple[int, int]]: Chronological sequence of
                cell coordinates.
                - str: A continuous string representing
                directions ('N', 'E', 'S', 'W').
        """

        explore = deque([self.entry])
        parents: dict[tuple[int, int], tuple[int, int]] = {}
        self.maze[self.entry].visited = True
        neighbors = [
            ('north', 0, -1),
            ('east', +1, 0),
            ('south', 0, +1),
            ('west', -1, 0)
        ]
        while explore:
            track = explore.popleft()
            if track == self.exit:
                return (self.build_path(parents))
            for directions, dx, dy in neighbors:
                x, y = track
                neighbor_cell = (x + dx, y + dy)
                if neighbor_cell in self.maze:
                    if self.maze[track].walls[directions] == 0:
                        if not self.maze[neighbor_cell].visited:
                            self.maze[neighbor_cell].visited = True
                            explore.append(neighbor_cell)
                            parents[neighbor_cell] = track
        print("ERROR: maze has no solution", file=sys.stderr)
        sys.exit(1)

    def build_path(
            self, parents: dict[tuple[int, int], tuple[int, int]]
            ) -> tuple[list[tuple[int, int]], str]:
        """
        Reconstructs the solution path by backtracking from exit to entry.

        Args:
            parents (dict[tuple[int, int], tuple[int, int]]): A dictionary
                mapping each explored cell to its corresponding parent cell.

        Returns:
            tuple[list[tuple[int, int]], str]: A tuple containing:
                - list[tuple[int, int]]: Chronological sequence of
                cell coordinates.
                - str: continuous string representing
                directions ('N', 'E', 'S', 'W').
        """

        path = []
        backtrack = self.exit
        while backtrack != self.entry:
            path.append(backtrack)
            backtrack = parents[backtrack]
        path.append(self.entry)
        path.reverse()
        convert_str = []
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            if y2 < y1:
                direction = 'N'
            elif x2 > x1:
                direction = 'E'
            elif y2 > y1:
                direction = 'S'
            elif x2 < x1:
                direction = 'W'
            else:
                continue
            convert_str.append(direction)
        return (path, ''.join(convert_str))

    def open_walls(self) -> None:
        """
        Breaks the maze perfection by creating random loops and shortcuts.

        Calculates a ratio of walls to break based on the original path length
        and removes blocking boundaries near the solution track without
        distorting frozen cells. Includes safety limits to prevent infinite
        loops on micro-sized mazes.
        """

        walls_to_break: int = (len(self.solution_path) * 12 // 100)
        if walls_to_break == 0:
            walls_to_break = 2

        total_cells: int = self.width * self.height
        max_breaks: int = total_cells // 3
        if max_breaks < 1:
            max_breaks = 1

        if walls_to_break > max_breaks:
            walls_to_break = max_breaks

        attempts: int = 0
        max_attempts: int = total_cells * 10

        directions: list[str] = ['north', 'east', 'south', 'west']
        while walls_to_break > 0 and attempts < max_attempts:
            cell: tuple[int, int] = random.choice(self.solution_path)
            next_dir: str = random.choice(directions)
            next_cell: tuple[str, str, tuple[int, int]]

            if next_dir == 'north':
                next_cell = ('north', 'south', (cell[0], cell[1] - 1))
            elif next_dir == 'east':
                next_cell = ('east', 'west', (cell[0] + 1, cell[1]))
            elif next_dir == 'south':
                next_cell = ('south', 'north', (cell[0], cell[1] + 1))
            else:
                next_cell = ('west', 'east', (cell[0] - 1, cell[1]))

            dir_act, dir_ngb, target_coord = next_cell
            new_col, new_row = target_coord

            if (
                (0 <= new_col < self.width and 0 <= new_row < self.height)
                and not self.maze[target_coord].freeze
            ):
                if self.maze[cell].walls[dir_act] == 1:
                    self.maze[cell].walls[dir_act] = 0
                    self.maze[target_coord].walls[dir_ngb] = 0
                    walls_to_break -= 1
            attempts += 1

    def get_hex(self) -> None:
        """
        Converts final wall states to hexadecimal and saves them
        to output_file.
        """

        valid_hex: str = '0123456789ABCDEF'
        for cell in self.maze:
            n = self.maze[cell].walls['north']
            e = self.maze[cell].walls['east']
            s = self.maze[cell].walls['south']
            w = self.maze[cell].walls['west']
            number: int = n + e * 2 + s * 4 + w * 8
            hex: str = valid_hex[number]
            self.maze[cell].hex = hex

    def get_output(self) -> None:
        """
        Writes the hexadecimal grid layout and metadata to the output file.
        """

        with open(self.output_file, "w") as file:
            y = 0
            while y < self.height:
                x = 0
                while x < self.width:
                    file.write(self.maze[(x, y)].hex)
                    x += 1
                file.write("\n")
                y += 1
            file.write("\n")
            file.write(f"{self.entry[0]},{self.entry[1]}\n")
            file.write(f"{self.exit[0]},{self.exit[1]}\n")
            file.write(self.solution_str)

    def solve_maze(self) -> None:
        """
        Coordinates the main resolution and final file dump pipeline.

        Solves the original maze structure, applies additional pathways if
        imperfect mode is requested, re-evaluates the optimal solution,
        and triggers the writing workflow.
        """
        self.reset_visited()
        self.solution_path, self.solution_str = self.bfs()
        if self.perfect:
            self.get_hex()
            self.get_output()
        else:
            self.reset_visited()
            self.open_walls()
            self.solution_path, self.solution_str = self.bfs()
            self.get_hex()
            self.get_output()
