*This project has been created as part of the 42 curriculum by albben-a, jezambra.*

# A-Maze-ing

## Description

**A-Maze-ing** is a collaborative Python project from the 42 curriculum focused on procedural maze generation, graph algorithms, modular software design, and graphical visualization.

The program generates a maze from a configuration file, writes it to an output file using a hexadecimal wall representation, displays it graphically, and computes the shortest path between the entrance and the exit.

The project was designed with modularity in mind by separating the maze generation and solving logic into an independent Python package that can be reused in future projects.

---

# Instructions

## Requirements

The project requires:

- Python 3.10 or later
- pygame
- make

Install the dependencies:

```bash
make install
```

Run the project:

```bash
make run
```

or directly:

```bash
python3 a_maze_ing.py config.txt
```

The program receives a single configuration file describing the maze to generate and validates all parameters before creating the maze.

---

# Configuration File

The maze is configured using a plain text file containing one `KEY=VALUE` pair per line.

Example:

```text
WIDTH=20
HEIGHT=20
ENTRY=1,0
EXIT=15,16
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=1234
```

## Configuration Parameters

| Parameter | Description |
|-----------|-------------|
| `WIDTH` | Width of the maze (cells) |
| `HEIGHT` | Height of the maze |
| `ENTRY` | Entrance coordinates `(x,y)` |
| `EXIT` | Exit coordinates `(x,y)` |
| `OUTPUT_FILE` | Output filename |
| `PERFECT` | Generates a perfect maze when `True` |
| `SEED` | Seed used for deterministic generation |

---

# Output File

The generated maze is written to the output file using the hexadecimal encoding required by the subject.

Each hexadecimal digit represents the walls of one cell:

| Bit | Wall |
|-----|------|
| 0 | North |
| 1 | East |
| 2 | South |
| 3 | West |

After the maze representation, the file also contains:

- Entry coordinates
- Exit coordinates
- Shortest path using the letters `N`, `E`, `S` and `W`

---

# Algorithms

## Maze Generation — Depth-First Search (DFS)

Maze generation is based on the **Depth-First Search (DFS)** recursive backtracking algorithm.

Starting from the entrance, the algorithm visits neighboring cells in random order while carving passages between them. Whenever it reaches a dead end, it backtracks until it finds a cell with unexplored neighbors.

### Why DFS?

DFS was selected because it:

- is simple and efficient to implement;
- generates connected mazes with natural-looking corridors;
- guarantees that every cell is reachable;
- naturally produces perfect mazes when required.

Its time complexity is **O(n)**, where *n* is the number of cells.

---

## Maze Solving — Breadth-First Search (BFS)

The shortest path is computed using **Breadth-First Search (BFS)**.

Beginning at the entrance, BFS explores the maze level by level until it reaches the exit. The path is then reconstructed from the visited nodes.

### Why BFS?

BFS guarantees the **shortest path** in an unweighted graph, making it the most appropriate algorithm for maze solving.

Its complexity is also **O(n)**.

---

# Perfect vs Non-Perfect Mazes

The project supports two generation modes.

### PERFECT=True

A **perfect maze** contains exactly one possible path between any two cells. There are no loops, making the maze equivalent to a spanning tree.

### PERFECT=False

The default mode generates a maze suitable for a Pac-Man-like game.

Additional corridors are opened to create loops, allowing multiple possible routes between locations while maintaining full connectivity.

---

# Reusable Package

One of the project requirements is to make the maze generation reusable.

The maze generation and solving logic are isolated inside an independent Python package built using the project's `pyproject.toml`.

The package can be built into a standard Python distribution (`.whl` or `.tar.gz`) and installed in another project using `pip`.

Example:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

Once installed, the generator can be imported independently of the graphical interface:

```python
from mazegen import MazeGenerator

generator = MazeGenerator(width=20, height=20, seed=1234)
maze = generator.generate()
solution = generator.solve()
```

This modular architecture separates:

- maze generation;
- maze solving;
- configuration parsing;
- graphical interface.

This makes the generation package reusable without modifying its internal implementation.

---

# Display Features

The graphical interface includes several interactive options:

- Generate a new maze
- Show or hide the solution
- Animate the solution
- Change maze colors
- Change wall colors
- Exit the application

These features make it easier to visualize both the generated maze and the pathfinding process.

---

# Team & Project Management

## Roles

### Alba (albben-a)

Responsible for:

- configuration file parsing;
- DFS maze generation;
- graphical maze rendering.

### Jesús (jezambra)

Responsible for:

- BFS maze solving;
- Makefile;
- solution animation;
- keyboard controls and display options.

---

## Planning & Evolution

Before starting development, we agreed on a common project architecture, shared data structures, and naming conventions. This allowed both team members to work independently while ensuring compatibility between modules.

Throughout the project, we regularly reviewed each other's work and refined the interfaces between the generation, solving, and visualization components as new requirements emerged.

---

## Retrospective

### What worked well

Separating the project into reusable modules allowed parallel development with minimal conflicts.

Defining the maze representation before implementing the algorithms made integration significantly easier.

### What could be improved

Although the initial planning was effective, some interfaces evolved during development, requiring minor refactoring. Defining every module interface in greater detail from the beginning would have reduced these changes.

---

## Tools Used

The following tools were used throughout the project:

- Visual Studio Code
- Git
- GitHub
- Python virtual environments

---

# Resources

## Documentation & References

- A-Maze-ing subject :contentReference[oaicite:0]{index=0}
- Python Official Documentation
- pygame Documentation
- DFS and BFS algorithm documentation
- Graph Theory references
- Peer-to-peer discussions
- https://noreply.gitbook.io/born2beroot (used as inspiration for project organization and documentation style)

---

## Use of Artificial Intelligence

Artificial Intelligence was used to:

- clarify specific Python concepts;
- discuss alternative approaches for maze generation and graph traversal;
- design additional test cases;
- assist in writing and reviewing the project documentation.

AI was **not used to generate the implementation of the maze generation, maze solving, configuration parser, or graphical interface**. All code was designed, implemented, tested, and reviewed by the project authors to ensure full understanding of the project and compliance with the learning objectives of the 42 curriculum.
---

# Algorithms

## Maze Generation — Depth-First Search (DFS)

The maze is generated using the **Depth-First Search (DFS)** recursive backtracking algorithm.

Starting from the entrance, the algorithm visits neighboring cells randomly while carving passages between them. When a dead end is reached, it backtracks until it finds a cell with unexplored neighbors.

### Why DFS?

DFS was chosen because it:

- is simple and efficient to implement;
- generates connected mazes with a natural appearance;
- produces long corridors and relatively few dead ends;
- guarantees that every cell is reachable.

Its time complexity is **O(n)**, where *n* is the number of cells in the maze.

---

## Maze Solving — Breadth-First Search (BFS)

The maze is solved using **Breadth-First Search (BFS)**.

Starting from the entrance, BFS explores the maze level by level until the exit is reached. Once found, the shortest path is reconstructed and displayed.

### Why BFS?

BFS guarantees the **shortest path** in an unweighted graph, making it an ideal choice for maze solving.

Its time complexity is also **O(n)**.

---

# Reusable Architecture

One of the project's main goals was to create reusable code.

The maze generation and solving logic are isolated inside an independent Python package. Thanks to the project's `pyproject.toml`, this package can be imported into other Python projects without modifying its internal implementation.

This modular architecture separates:

- maze generation;
- maze solving;
- configuration parsing;
- graphical interface.

As a result, the algorithms can be reused independently from the graphical application, making future extensions and maintenance significantly easier.

---

# Display Features

The graphical interface includes several interactive features:

- Generate a new random maze
- Show or hide the solution
- Change maze colors
- Change wall colors
- Animate the solution
- Exit the application

These options allow users to visualize the generation and solving process in different ways.

---

# Team & Project Management

## Roles

### Alba (albben-a)

Responsible for:

- configuration file parsing
- maze generation (DFS)
- graphical maze rendering

### Jesús (jezambra)

Responsible for:

- maze solving (BFS)
- Makefile
- solution animation
- keyboard controls and display options

---

## Planning & Evolution

At the beginning of the project, we agreed on a common project structure, naming conventions, and data representation. This allowed both team members to work independently on different modules while ensuring seamless integration.

During development, we regularly reviewed each other's work and adapted some interfaces to simplify communication between the generation, solving, and visualization modules.

---

## Retrospective

### What worked well

Separating the project into independent modules allowed us to work in parallel without conflicts. Defining the data structures early greatly simplified integration and debugging.

Keeping the maze algorithms inside a reusable package also improved the overall organization of the project.

### What could be improved

Although the initial planning was effective, some interface changes during development required minor refactoring. Defining all module interfaces in greater detail from the beginning would have reduced these adjustments.

---

## Tools Used

The following tools were used throughout the project:

- **Visual Studio Code** for development
- **Git** for version control
- **GitHub** for collaboration, code reviews, and merging
- **Python virtual environments** for dependency management

---

# Resources

## Documentation & References

- A-Maze-ing subject
- Python official documentation
- pygame documentation
- Depth-First Search (DFS) documentation
- Breadth-First Search (BFS) documentation
- Graph theory references
- Peer-to-peer discussions

---

## Use of Artificial Intelligence

Artificial Intelligence was used to:

- clarify specific Python concepts;
- discuss algorithmic alternatives for maze generation and solving;
- assist in writing project documentation.

AI was **not used to generate the core implementation of the maze generation, solving algorithms, or graphical interface**. All code was designed, implemented, tested, and integrated by the project authors in accordance with the learning objectives of the 42 curriculum.
