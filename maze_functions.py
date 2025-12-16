# maze_module.py
import random
import heapq
import time
import os
from collections import deque

WALL = 1
PATH = 0

class Maze:
    def __init__(self, rows: int = 21, cols: int = 21):
        # prefer odd dimensions for classic cell/wall layout
        self.rows = rows if rows % 2 == 1 else rows + 1
        self.cols = cols if cols % 2 == 1 else cols + 1
        self.grid = [[WALL for _ in range(self.cols)] for _ in range(self.rows)]

    #  Prim's algorithm (cell-based)
    def generate_prim(self, seed: int = 0):
        if seed != 0:
            random.seed(seed)
        # Start at (1,1)
        start = (1, 1)
        self.grid[start[0]][start[1]] = PATH

        # frontier holds walls adjacent to carved cell, stored as (wall_r, wall_c, cell_r, cell_c)
        frontier = []
        def add_frontier(r, c):
            for dr, dc in [(2,0),(-2,0),(0,2),(0,-2)]:
                nr, nc = r + dr, c + dc
                if 1 <= nr < self.rows-1 and 1 <= nc < self.cols-1:
                    if self.grid[nr][nc] == WALL:
                        # store candidate cell (nr,nc) and the cell that 'connects' it (r,c)
                        frontier.append((nr, nc, r, c))

        add_frontier(*start)

        while frontier:
            idx = random.randrange(len(frontier))
            wr, wc, pr, pc = frontier.pop(idx)
            # if target cell still wall (not yet carved)
            if self.grid[wr][wc] == WALL:
                # carve target cell
                self.grid[wr][wc] = PATH
                # carve middle wall between pr,pc and wr,wc
                midr = (wr + pr) // 2
                midc = (wc + pc) // 2
                self.grid[midr][midc] = PATH
                add_frontier(wr, wc)

    #  utility
    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_path(self, r, c):
        return self.in_bounds(r, c) and self.grid[r][c] == PATH

    def neighbors(self, r, c):
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if self.is_path(nr, nc):
                yield (nr, nc)

    #  display for debugging
    #TODO Delete once Streamlit interface is made
    def display(self, visited=set(), current=None, final_path=set()):
        # terminal clear
        os.system("cls" if os.name == "nt" else "clear")
        rows = []
        for r in range(self.rows):
            row = ""
            for c in range(self.cols):
                if (r, c) == current:
                    row += "○○"  # current node
                elif (r, c) in final_path:
                    row += "●●"  # final path
                elif (r, c) in visited:
                    row += "··"  # visited nodes
                elif self.grid[r][c] == WALL:
                    row += "██"
                else:
                    row += "  "
            rows.append(row)
        print("\n".join(rows))

    #  Step generators for solvers 

    def solve_bfs_steps(self, start, goal):
        """BFS that yields (visited_set, current, path_so_far) on each node visit"""
        q = deque([start])
        visited = set([start])
        parent = {}

        # yield initial state
        yield visited, start, set()

        while q:
            cur = q.popleft()
            # when we visit cur, yield
            yield visited, cur, set()
            if cur == goal:
                break
            for nxt in self.neighbors(*cur):
                if nxt not in visited:
                    visited.add(nxt)
                    parent[nxt] = cur
                    q.append(nxt)
                    yield visited, nxt, set()  # show addition to visited

        # reconstruct path and yield it as final_path
        final_path = set()
        if goal in parent or start == goal:
            node = goal
            final_path.add(node)
            while node != start:
                node = parent.get(node)
                if node is None:
                    break
                final_path.add(node)
        yield visited, goal, final_path

    def solve_dfs_steps(self, start, goal):
        """DFS (iterative) that yields on visits"""
        stack = [start]
        visited = set()
        parent = {}

        yield visited, None, set()

        while stack:
            cur = stack.pop()
            if cur in visited:
                continue
            visited.add(cur)
            yield visited, cur, set()
            if cur == goal:
                break
            for nxt in self.neighbors(*cur):
                if nxt not in visited:
                    parent[nxt] = cur
                    stack.append(nxt)
                    # optionally yield when pushing neighbor
                    yield visited, nxt, set()

        final_path = set()
        if goal in parent or start == goal:
            node = goal
            final_path.add(node)
            while node != start:
                node = parent.get(node)
                if node is None:
                    break
                final_path.add(node)
        yield visited, goal, final_path

    def solve_dijkstra_steps(self, start, goal):
        """Dijkstra yields steps similar to A* (grid unweighted so same as BFS but via PQ)"""
        pq = [(0, start)]
        dist = {start: 0}
        parent = {}
        visited = set()
        yield visited, None, set()
        while pq:
            d, cur = heapq.heappop(pq)
            if cur in visited:
                continue
            visited.add(cur)
            yield visited, cur, set()
            if cur == goal:
                break
            for nxt in self.neighbors(*cur):
                nd = d + 1
                if nxt not in dist or nd < dist[nxt]:
                    dist[nxt] = nd
                    parent[nxt] = cur
                    heapq.heappush(pq, (nd, nxt))
                    yield visited, nxt, set()

        final_path = set()
        if goal in parent or start == goal:
            node = goal
            final_path.add(node)
            while node != start:
                node = parent.get(node)
                if node is None:
                    break
                final_path.add(node)
        yield visited, goal, final_path

    def solve_astar_steps(self, start, goal):
        """A* (Manhattan) generator yielding steps"""
        def h(a, b):
            return abs(a[0]-b[0]) + abs(a[1]-b[1])
        pq = [(h(start, goal), 0, start)]
        gscore = {start: 0}
        parent = {}
        visited = set()
        yield visited, None, set()
        while pq:
            _, g, cur = heapq.heappop(pq)
            if cur in visited:
                continue
            visited.add(cur)
            yield visited, cur, set()
            if cur == goal:
                break
            for nxt in self.neighbors(*cur):
                tentative = g + 1
                if nxt not in gscore or tentative < gscore[nxt]:
                    gscore[nxt] = tentative
                    parent[nxt] = cur
                    priority = tentative + h(nxt, goal)
                    heapq.heappush(pq, (priority, tentative, nxt))
                    yield visited, nxt, set()

        final_path = set()
        if goal in parent or start == goal:
            node = goal
            final_path.add(node)
            while node != start:
                node = parent.get(node)
                if node is None:
                    break
                final_path.add(node)
        yield visited, goal, final_path
