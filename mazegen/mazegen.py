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
        self.og_center: tuple[int, int] = ((self.width // 2),
                                           (self.height // 2))
        self.ft_center: tuple[int, int]
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

        middle_col = (self.width // 2)
        middle_row = (self.height // 2)
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
            if (
                self.entry not in frozen
                and self.exit not in frozen
                and self.og_center not in frozen

            ):
                self.ft_center = coord
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
        """Transforms the maze into a fully connected Pac-Man board.

        Carves corners, connects the center vertically to the 42 track,
        injects loops along the path, and iteratively eliminates 100%
        of dead-ends to secure the project bonus.
        """
        width, height = self.width, self.height

        corners = [(0, 0), (width - 1, 0), (0, height - 1),
                   (width - 1, height - 1)]
        for (x, y) in corners:
            if x == 0 and y == 0:
                self.maze[(0, 0)].walls['south'] = 0
                self.maze[(0, 1)].walls['north'] = 0
                self.maze[(0, 0)].walls['east'] = 0
                self.maze[(1, 0)].walls['west'] = 0
            elif x == width - 1 and y == 0:
                self.maze[(width - 1, 0)].walls['south'] = 0
                self.maze[(width - 1, 1)].walls['north'] = 0
                self.maze[(width - 1, 0)].walls['west'] = 0
                self.maze[(width - 2, 0)].walls['east'] = 0
            elif x == 0 and y == height - 1:
                self.maze[(0, height - 1)].walls['north'] = 0
                self.maze[(0, height - 2)].walls['south'] = 0
                self.maze[(0, height - 1)].walls['east'] = 0
                self.maze[(1, height - 1)].walls['west'] = 0
            elif x == width - 1 and y == height - 1:
                self.maze[(width - 1, height - 1)].walls['north'] = 0
                self.maze[(width - 1, height - 2)].walls['south'] = 0
                self.maze[(width - 1, height - 1)].walls['west'] = 0
                self.maze[(width - 2, height - 1)].walls['east'] = 0

        mid_x, mid_y = self.og_center
        act_y = mid_y
        while act_y > 0:
            current_coord = (mid_x, act_y)
            next_coord = (mid_x, act_y - 1)

            current_cell = self.maze[current_coord]
            next_cell = self.maze[next_coord]

            if current_cell.freeze or next_cell.freeze:
                break

            current_cell.walls['north'] = 0
            next_cell.walls['south'] = 0
            act_y -= 1

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

            if next_dir == 'north':
                next_cell_data = ('north', 'south', (cell[0], cell[1] - 1))
            elif next_dir == 'east':
                next_cell_data = ('east', 'west', (cell[0] + 1, cell[1]))
            elif next_dir == 'south':
                next_cell_data = ('south', 'north', (cell[0], cell[1] + 1))
            else:
                next_cell_data = ('west', 'east', (cell[0] - 1, cell[1]))

            dir_act, dir_ngb, target_coord = next_cell_data
            new_col, new_row = target_coord

            if (0 <= new_col < self.width and 0 <= new_row < self.height):
                if not self.maze[target_coord].freeze:
                    if self.maze[cell].walls[dir_act] == 1:
                        self.maze[cell].walls[dir_act] = 0
                        self.maze[target_coord].walls[dir_ngb] = 0
                        walls_to_break -= 1
            attempts += 1

        while True:
            dead_ends_found = False
            for (x, y), c in self.maze.items():
                if c.freeze:
                    continue

                closed_walls = list(c.walls.values()).count(1)
                if closed_walls == 3:
                    pos_breaks = []
                    if c.walls['north'] == 1 and y > 0:
                        if not self.maze[(x, y - 1)].freeze:
                            pos_breaks.append(('north', 'south', (x, y - 1)))
                    if c.walls['east'] == 1 and x < width - 1:
                        if not self.maze[(x + 1, y)].freeze:
                            pos_breaks.append(('east', 'west', (x + 1, y)))
                    if c.walls['south'] == 1 and y < height - 1:
                        if not self.maze[(x, y + 1)].freeze:
                            pos_breaks.append(('south', 'north', (x, y + 1)))
                    if c.walls['west'] == 1 and x > 0:
                        if not self.maze[(x - 1, y)].freeze:
                            pos_breaks.append(('west', 'east', (x - 1, y)))

                    if pos_breaks:
                        dead_ends_found = True
                        d_act, d_ngb, (nx, ny) = random.choice(pos_breaks)
                        self.maze[(x, y)].walls[d_act] = 0
                        self.maze[(nx, ny)].walls[d_ngb] = 0

            if not dead_ends_found:
                break

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
