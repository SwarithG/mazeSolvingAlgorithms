# Maze Generator & Solver

This is a Streamlit-based web application for generating and solving mazes. It uses Prim's algorithm to generate mazes and supports solving with BFS, DFS, Dijkstra, and A* algorithms.

## Prerequisites

- Python 3.7 or higher
- Streamlit library
- The `maze_functions.py` module (included in this directory)

## Installation

1. Clone or download this repository.
2. Install dependencies:
   ```
   pip install streamlit
   ```
3. Ensure `maze_functions.py` is in the same directory as `app.py`.

## Usage

1. Run the app:
   ```
   streamlit run app.py
   ```
2. Open the provided URL in your browser (usually http://localhost:8501).

### Controls

- **Rows/Columns**: Adjust maze size (odd numbers recommended for proper generation).
- **Random Seed**: Set to 0 for random mazes, or a specific number for reproducible results.
- **Solver Algorithm**: Choose from BFS, DFS, Dijkstra, or A*.
- **Animation Speed**: Control how fast the solving animation runs.
- **Generate Maze**: Create a new maze with the current settings.
- **Solve Maze**: Run the selected algorithm to find a path from start to goal.

### Maze Display

- Black: Open paths
- White: Walls
- Green: Visited cells during solving
- Orange: Current position
- Red: Final path

The maze starts at (1,1) and ends at (rows-2, cols-2).

## Features

- Interactive maze generation and solving
- Multiple solving algorithms
- Animated solving process
- Customizable maze size and parameters

For more details, see the code in `app.py` and `maze_functions.py`.