````markdown
*This project has been created as part of the 42 curriculum by albben-a, jezambra.*

# A-Maze-ing

## Description

**A-Maze-ing** is a collaborative Python project from the 42 curriculum focused on procedural maze generation, pathfinding algorithms, modular software design, and graphical visualization.

The project generates a maze from a configuration file, displays it in a graphical window, and optionally computes and animates the shortest path between the maze entrance and exit. The application was designed with modularity in mind, separating the maze generation and solving logic into a reusable Python package that can be integrated into other projects.

---

# Instructions

## Requirements

The project requires:

- Python 3
- pygame
- make

Install the dependencies:

```bash
pip install -r requirements.txt
```

Compile and launch the project:

```bash
make
```

or

```bash
python3 src/main.py config.cfg
```

---

## Configuration File

The maze is generated from a configuration file with the following format:

```text
WIDTH=20
HEIGHT=20
ENTRY=1,0
EXIT=15,16
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=1234
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `WIDTH` | Width of the maze |
| `HEIGHT` | Height of the maze |
| `ENTRY` | Entrance coordinates |
| `EXIT` | Exit coordinates |
| `OUTPUT_FILE` | Output file where the maze is stored |
| `PERFECT` | Generates a perfect maze when enabled |
| `SEED` | Seed used for deterministic generation |

---

## Usage

Run the program by providing a configuration file:

```bash
python3 src/main.py config.cfg
```

The application generates the maze, displays it in a graphical window, and allows several interactive options.

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
````
