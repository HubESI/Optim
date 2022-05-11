from collections import deque
from typing import List, Set, Tuple

from coloring import Coloring, Graph, timer


class BranchAndBound(Coloring):
    def __init__(self, g: Graph) -> None:
        super().__init__(g)
        self.greedy_coloring()

    def create_node(
        self, current_vertex: int, state: List[int], eval: int
    ) -> "BranchAndBound.Node":
        return self.Node(self, current_vertex, state, eval)

    class Node:
        def __init__(
            self,
            outer: "BranchAndBound",
            current_vertex: int,
            state: List[int],
            eval: int,
        ) -> None:
            self.outer = outer
            self.current_vertex = current_vertex
            self.state = state
            self.eval = eval

        @classmethod
        def child_node(
            cls, node: "BranchAndBound.Node", color: int, eval: int
        ) -> "BranchAndBound.Node":
            current_vertex = (
                node.current_vertex + 1
                if node.current_vertex < node.outer.g.order
                else None
            )
            state = node.state.copy()
            state[node.current_vertex - 1] = color
            return cls(node.outer, current_vertex, state, eval)

    @timer
    def solve(self) -> None:
        bound = self.solution[0]

        def colors_info(
            current_vertex: int, state: List[int]
        ) -> Tuple[Set[int], Set[int]]:
            used_colors = set(state)
            used_colors.remove(None)
            possible_colors = used_colors.copy()
            unused_colors = set(range(1, self.g.order + 1)).difference(used_colors)
            for _ in range(bound - len(used_colors)):
                possible_colors.add(unused_colors.pop())
            for vi in range(self.g.order):
                if state[vi] and self.adj_mat[current_vertex - 1][vi]:
                    possible_colors.discard(state[vi])
            return possible_colors, used_colors

        active_nodes = deque()
        active_nodes.append(self.create_node(1, [None] * self.g.order, 0))
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
                active_nodes.append(self.Node.child_node(node, color, eval))

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
