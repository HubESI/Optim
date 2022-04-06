import time
from collections import deque
import sys
from queue import PriorityQueue
from functools import total_ordering

from graph import Graph


def timer(func):
    def wrapper_timer(*args, **kwargs):
        tic = time.process_time()
        value = func(*args, **kwargs)
        toc = time.process_time()
        return value, toc - tic

    return wrapper_timer


class Coloring:
    def __init__(self, g):
        self.g = g
        self.solution = len(g.adj_mat), [ci + 1 for ci in range(len(g.adj_mat))]

    @timer
    def branch_and_bound(self):
        adj_mat = self.g.adj_mat
        n = len(adj_mat)
        bound = self.solution[0]
        vertices_nexts = [v + 1 for v in range(1, n)] + [None]

        def colors_info(current_vertex, state):
            used_colors = set(state)
            used_colors.remove(None)
            possible_colors = used_colors.copy()
            unused_colors = set(range(1, n + 1)).difference(used_colors)
            for _ in range(bound - len(used_colors)):
                possible_colors.add(unused_colors.pop())
            for vi in range(n):
                if state[vi] and adj_mat[current_vertex - 1][vi]:
                    possible_colors.discard(state[vi])
            return possible_colors, used_colors

        class Node:
            def __init__(self, current_vertex, eval, state):
                self.current_vertex = current_vertex
                self.eval = eval
                self.state = state

            @classmethod
            def child_node(cls, node, color, eval):
                new_state = node.state.copy()
                new_state[node.current_vertex - 1] = color
                return cls(vertices_nexts[node.current_vertex - 1], eval, new_state)

        active_nodes = deque()
        active_nodes.append(Node(1, 0, [None] * n))
        while active_nodes:
            node = active_nodes.pop()
            if node.eval >= bound:
                continue
            if node.current_vertex is None:
                bound = node.eval
                self.solution = (bound, node.state)
                continue
            possible_colors, used_colors = colors_info(node.current_vertex, node.state)
            for color in sorted(possible_colors, reverse=True):
                eval = node.eval if color in used_colors else node.eval + 1
                if eval >= bound:
                    continue
                active_nodes.append(Node.child_node(node, color, eval))

    @timer
    def min_color_heuristic(self):
        adj_mat = self.g.adj_mat
        n = len(adj_mat)
        vertices_nexts = [v + 1 for v in range(1, n)] + [None]

        def available_colors(current_vertex, state):
            colors = set(range(1, n + 1))
            for vi in range(n):
                if state[vi] and adj_mat[current_vertex - 1][vi]:
                    colors.discard(state[vi])
            return colors

        @total_ordering
        class Node:
            def __init__(self, current_vertex, state):
                self.current_vertex = current_vertex
                self.state = state

            @classmethod
            def child_node(cls, node, color):
                new_state = node.state.copy()
                new_state[node.current_vertex - 1] = color
                return cls(vertices_nexts[node.current_vertex - 1], new_state)

            @property
            def last_color(self):
                if self.current_vertex:
                    return (
                        self.state[self.current_vertex - 2]
                        if self.current_vertex >= 2
                        else 0
                    )
                return self.state[-1]

            def __eq__(self, other):
                return self.last_color == other.last_color

            def __lt__(self, other):
                return self.last_color < other.last_color

        active_nodes = PriorityQueue()
        active_nodes.put(Node(1, [None] * n))
        while active_nodes:
            node = active_nodes.get()
            if node.current_vertex is None:
                self.solution = (len(set(node.state)), node.state)
                break
            colors = available_colors(node.current_vertex, node.state)
            for color in colors:
                active_nodes.put(Node.child_node(node, color))

    def greedy_coloring(self):
        n = len(self.g.adj_mat)
        solution = [-1] * n
        # Assign the first color to first vertex
        solution[0] = 1
        # A temporary array to store the available colors.
        # False value of available[c] would mean that the
        # color c is assigned to one of its adjacent vertices
        available_colors = [True] * n
        # Assign colors to remaining n-1 vertices
        for u in range(1, n):
            # Process all adjacent vertices and
            # flag their colors as unavailable
            for i in range(n):
                if self.g.adj_mat[u][i] and solution[i] != -1:
                    available_colors[solution[i] - 1] = False
            # Find the first available color
            c = available_colors.index(True) + 1
            # Assign the found color
            solution[u] = c
            # Reset the values back to false
            # for the next iteration
            available_colors = [True] * n
        self.solution = len(set(solution)), solution

    def to_file(self, file_path, *args, **kwargs):
        with open(file_path, "w") as f:
            for c in args:
                f.write(f"c {c}\n")
            for _, c in kwargs.items():
                f.write(f"c {c}\n")
            f.write(f"s col {self.solution[0]}\n")
            for vi in range(len(self.solution[1])):
                f.write(f"l {vi+1} {self.solution[1][vi]}\n")


if __name__ == "__main__":
    try:
        input_file = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <input_file> [<output_file>]")
    try:
        output_file = sys.argv[2]
    except IndexError:
        output_file = f"{input_file}.min_color_heuristic.sol"
    g = Graph.from_file(input_file)
    col = Coloring(g)
    t = col.min_color_heuristic()[-1]
    col.to_file(
        output_file,
        graph_info=f"Coloring the graph defined in '{input_file}'",
        method_time_info=f"Minimal color heuristic in {t:0.6f} seconds",
    )
