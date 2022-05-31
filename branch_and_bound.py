import sys
from collections import deque
from typing import List, Set

from coloring import Coloring, Graph, timer


class BranchAndBound(Coloring):
    def __init__(self, g: Graph) -> None:
        super().__init__(g)
        self.greedy_coloring()

    def create_node(
        self, vertex: int, state: List[int], newest_color: int, eval: int
    ) -> "BranchAndBound.Node":
        return self.Node(self, vertex, state, newest_color, eval)

    class Node:
        def __init__(
            self,
            outer: "BranchAndBound",
            vertex: int,
            state: List[int],
            newest_color: int,
            eval: int,
        ) -> None:
            self.outer = outer
            self.vertex = vertex
            self.state = state
            self.newest_color = newest_color
            self.eval = eval

        @classmethod
        def child_node(
            cls, parent: "BranchAndBound.Node", color: int, eval: int
        ) -> "BranchAndBound.Node":
            vertex = parent.vertex + 1 if parent.vertex < parent.outer.g.order else None
            state = parent.state.copy()
            state[parent.vertex - 1] = color
            newest_color = max(parent.newest_color, color)
            return cls(parent.outer, vertex, state, newest_color, eval)

    @timer
    def solve(self) -> None:
        bound = self.solution[0]

        def possible_used_colors(current_vertex: int, state: List[int]) -> Set[int]:
            used_colors = set(state)
            used_colors.remove(None)
            for vi in range(self.g.order):
                if state[vi] and self.adj_mat[current_vertex - 1][vi]:
                    used_colors.discard(state[vi])
            return used_colors

        active_nodes = deque()
        active_nodes.append(self.create_node(1, [None] * self.g.order, 0, 0))
        while active_nodes:
            node = active_nodes.pop()
            if node.eval >= bound:
                continue
            if node.vertex is None:
                bound = node.eval
                self.solution = (bound, node.state)
                continue
            possible_used = possible_used_colors(node.vertex, node.state)
            for color in possible_used:
                active_nodes.append(self.Node.child_node(node, color, node.eval))
            if node.eval + 1 < bound:
                active_nodes.append(
                    self.Node.child_node(node, node.newest_color + 1, node.eval + 1)
                )

    def greedy_coloring(self) -> None:
        solution = [-1] * self.g.order
        # Assign the first color to first vertex
        solution[0] = 1
        # A temporary array to store the available colors.
        # False value of available[c] would mean that the
        # color c is assigned to one of its adjacent vertices
        available_colors = [True] * self.g.order
        # Assign colors to remaining n-1 vertices
        for u in range(1, self.g.order):
            # Process all adjacent vertices and
            # flag their colors as unavailable
            for i in range(self.g.order):
                if self.adj_mat[u][i] and solution[i] != -1:
                    available_colors[solution[i] - 1] = False
            # Find the first available color
            c = available_colors.index(True) + 1
            # Assign the found color
            solution[u] = c
            # Reset the values back to false
            # for the next iteration
            available_colors = [True] * self.g.order
        self.solution = len(set(solution)), solution


if __name__ == "__main__":
    try:
        input_file = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <input_file> [<output_file>]")
    try:
        output_file = sys.argv[2]
    except IndexError:
        output_file = f"{input_file}.branch_and_bound.sol"
    g = Graph.from_file(input_file)
    col = BranchAndBound(g)
    t = col.solve()[1]
    col.to_file(
        output_file,
        graph_info=f"Coloring the graph defined in '{input_file}'",
        method_time_info=f"Branch and Bound in {t:0.6f} seconds",
    )
