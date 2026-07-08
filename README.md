*This project has been created as part of the 42 curriculum by albben-a, jezambra.*

# A-Maze-ing

## Description

**A-Maze-ing** is a collaborative Python project from the 42 curriculum focused on procedural maze generation, graph algorithms, modular software design, and graphical visualization.

The program generates a maze from a configuration file, writes it to an output file using a hexadecimal wall representation, displays it in a graphical window, and computes the shortest path between the entrance and the exit.

The project was designed with modularity in mind by separating the maze generation and solving logic into an independent Python package that can be reused in future projects, while the graphical interface remains independent from the core algorithms.

---

# Instructions

## Requirements

The project requires:

- Python 3.10 or later
- MiniLibX (MLX)
- make

Compile the project:

```bash
make
```

Run the application:

```bash
make run
```

or directly:

```bash
python3 a_maze_ing.py config.txt
```

The program receives a configuration file describing the maze to generate and validates all parameters before creating and displaying it.

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
- The shortest path using the directions `N`, `E`, `S` and `W`

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

Beginning at the entrance, BFS explores the maze level by level until it reaches the exit. Once found, the shortest path is reconstructed by following the visited nodes.

### Why BFS?

BFS guarantees the **shortest path** in an unweighted graph, making it the ideal algorithm for maze solving.

Its complexity is also **O(n)**.

---

# Perfect vs Non-Perfect Mazes

The project supports two generation modes.

### PERFECT=True

A **perfect maze** contains exactly one possible path between any two cells. There are no loops, making the maze equivalent to a spanning tree.

### PERFECT=False

The default mode generates a maze better suited for a Pac-Man-like game.

Additional corridors are opened after generation to create loops, allowing multiple possible routes while keeping the maze fully connected.

---

# Reusable Package

One of the project requirements is to make the maze generation reusable.

The maze generation and solving logic are isolated inside an independent Python package built using the project's `pyproject.toml`.

The package can be distributed as a standard Python package (`.whl` or `.tar.gz`) and installed in any other Python project using `pip`.

Example:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

After installation, the package can be imported independently of the graphical application:

```python
from mazegen import MazeGenerator

generator = MazeGenerator()
generator.gen_maze()
generator.solve_maze()
```

The project is divided into four independent components:

- configuration parsing;
- maze generation;
- maze solving;
- graphical interface.

Only the graphical interface depends on **MiniLibX**. The reusable package contains no graphical code, allowing the algorithms to be integrated into other applications without modification.

---

# Graphical Interface

The graphical interface is implemented using **MiniLibX (MLX)**, the lightweight graphics library used throughout the 42 curriculum.

MLX provides a simple abstraction over the native windowing system and allows the application to:

- create and manage graphical windows;
- draw the maze cell by cell;
- display the computed solution;
- animate the shortest path;
- process keyboard events in real time;
- update the display dynamically without affecting the maze algorithms.

By separating the graphical layer from the generation and solving logic, the project follows a modular architecture where the algorithms remain reusable independently of the user interface.

---

# Display Features

The graphical application provides several interactive options:

- Generate a new random maze
- Show or hide the solution
- Animate the solution
- Change maze colors
- Change wall colors
- Exit the application

These options allow users to visualize both the maze generation and the pathfinding process in different ways.

---

# Team & Project Management

## Roles

### albben-a

Responsible for:

- configuration file parsing;
- DFS maze generation;
- graphical maze rendering.

### jezambra

Responsible for:

- BFS maze solving;
- Makefile;
- solution animation;
- keyboard controls and display options.

---

## Planning & Evolution

Before starting development, we agreed on a common project architecture, shared data structures, and naming conventions. This allowed both team members to work independently while ensuring compatibility between modules.

The maze package and the graphical interface were developed in parallel. Throughout the project we regularly reviewed each other's work and refined the interfaces between the different modules to simplify integration.

---

## Retrospective

### What worked well

Separating the project into reusable modules allowed parallel development with very few merge conflicts.

Defining the maze representation before implementing the algorithms greatly simplified the integration of the generation, solving, and visualization modules.

### What could be improved

Although the initial planning was effective, some interfaces evolved during development, requiring minor refactoring. Defining every interface in greater detail from the beginning would have reduced these adjustments.

---

## Tools Used

The following tools were used throughout the project:

- Visual Studio Code
- Git
- GitHub
- Python virtual environments
- MiniLibX (MLX)

---

# Resources

## Documentation & References

- A-Maze-ing subject
- Python Official Documentation
- MiniLibX Documentation
- Depth-First Search (DFS) documentation
- Breadth-First Search (BFS) documentation
- Peer-to-peer discussions

---

## Use of Artificial Intelligence

Artificial Intelligence was used to:

- clarify specific Python and graph theory concepts;
- design additional test cases;
- assist in writing and reviewing the project documentation.

AI was **not used to generate the implementation of the maze generation, maze solving, configuration parser, or graphical interface**. All code was designed, implemented, tested, and reviewed by the project authors to ensure full understanding of the project and compliance with the learning objectives of the 42 curriculum.
