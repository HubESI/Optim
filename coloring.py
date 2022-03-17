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
        bound = n
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
                new_state = list(node.state)
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

    def to_file(self, file_path="sol.col", *args):
        with open(file_path, "w") as f:
            for c in args:
                f.write(f"c {c}\n")
            f.write(f"s col {self.solution[0]}\n")
            for vi in range(len(self.solution[1])):
                f.write(f"l {vi+1} {self.solution[1][vi]}\n")


if __name__ == "__main__":
    g = Graph.from_file("sample.col")
    col = Coloring(g)
    t = col.branch_and_bound()[-1]
    col.to_file("sol.col", f"Branch and Bound in {t:0.6f} seconds")
