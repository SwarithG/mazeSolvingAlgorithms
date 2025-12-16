# app.py
import streamlit as st
import time
from maze_functions import Maze, WALL, PATH

# Streamlit Page Config
st.set_page_config(page_title="Maze Generator & Solver", layout="wide")

# Sidebar Controls
st.sidebar.header("Maze Settings")
rows = st.sidebar.slider("Rows", 5, 30, 21, step=2)
cols = st.sidebar.slider("Columns", 5, 30, 21, step=2)
seed = st.sidebar.number_input("Random Seed (0 = random)", value=0, step=1)
algorithm = st.sidebar.selectbox("Solver Algorithm", ["BFS", "DFS", "Dijkstra", "A*"])
speed = st.sidebar.slider("Animation Speed (seconds)", 0.007, 0.3, 0.03, step=0.01)

generate_button = st.sidebar.button("Generate Maze")
solve_button = st.sidebar.button("Solve Maze")

# Initialize Maze 
if 'maze' not in st.session_state:
    st.session_state.maze = Maze(rows, cols)

maze = st.session_state.maze

#Generate Maze
if generate_button:
    maze = Maze(rows, cols)
    maze.generate_prim(seed)
    st.session_state.maze = maze

#  Display Layout 
col1, col2 = st.columns([2,1])  # 1:2 ratio

with col1:
    maze_display = st.empty()  # container for maze display

def render_maze_html(maze, visited=set(), current=None, final_path=set()):
    """Render maze as HTML for Streamlit"""
    html = "<pre style='font-size:12px; line-height:12px;'>"
    for r in range(maze.rows):
        for c in range(maze.cols):
            if (r, c) == current:
                html += "<span style='color:orange'>██</span>"
            elif (r, c) in final_path:
                html += "<span style='color:red'>██</span>"
            elif (r, c) in visited:
                html += "<span style='color:green'>██</span>"
            elif maze.grid[r][c] == WALL:
                html += "<span style='color:white'>██</span>"
            else:
                html += "<span style='color:black'>██</span>"
        html += "\n"
    html += "</pre>"
    return html

#  Solve Maze 
if solve_button:
    start = (1,1)
    goal = (maze.rows-2, maze.cols-2)

    if algorithm == "BFS":
        step_generator = maze.solve_bfs_steps(start, goal)
    elif algorithm == "DFS":
        step_generator = maze.solve_dfs_steps(start, goal)
    elif algorithm == "Dijkstra":
        step_generator = maze.solve_dijkstra_steps(start, goal)
    elif algorithm == "A*":
        step_generator = maze.solve_astar_steps(start, goal)

    for visited, current, final_path in step_generator:
        maze_display.markdown(render_maze_html(maze, visited, current, final_path), unsafe_allow_html=True)
        time.sleep(speed)

#  Initial Display 
if not solve_button:
    maze_display.markdown(render_maze_html(maze), unsafe_allow_html=True)
