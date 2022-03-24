import time
from collections import deque

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
        vertices_nexts = [vi + 2 for vi in range(n - 1)] + [None]

        def colors_info(current_vertex, state):
            possible_colors = set(range(1, bound + 1))
            used_colors = set()
            for vi in range(n):
                if state[vi]:
                    used_colors.add(state[vi])
                    if adj_mat[current_vertex - 1][vi]:
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
            possible_colors, used_colors = colors_info(node.current_vertex, node.state)
            for color in sorted(possible_colors, reverse=True):
                eval = node.eval if color in used_colors else node.eval + 1
                if eval >= bound:
                    continue
                child_node = Node.child_node(node, color, eval)
                if child_node.current_vertex:
                    active_nodes.append(child_node)
                else:
                    bound = eval
                    self.solution = (eval, child_node.state)

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

    def to_file(self, file_path="sol.col", *args, **kwargs):
        with open(file_path, "w") as f:
            for c in args:
                f.write(f"c {c}\n")
            for _, c in kwargs.items():
                f.write(f"c {c}\n")
            f.write(f"s col {self.solution[0]}\n")
            for vi in range(len(self.solution[1])):
                f.write(f"l {vi+1} {self.solution[1][vi]}\n")


if __name__ == "__main__":
    g = Graph.from_file("queen5_5.col")
    col = Coloring(g)
    col.greedy_coloring()
    t = col.branch_and_bound()[-1]
    col.to_file(time_info=f"Branch and Bound in {t:0.6f} seconds")
